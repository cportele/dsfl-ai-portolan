#!/bin/sh
# Builds the Portolan catalog (GeoParquet + STAC) of the BAG, BGT, wijkenbuurten and postcode6
# data of the dsfl-ai APIs into catalog/ of this repository.
#
#   scripts/build.sh            export from the database, then build the metadata
#   scripts/build.sh --docs     only rebuild the metadata and the docs from the existing parquet files
#
# Environment:
#   DSFL_AI      checkout of https://github.com/cportele/dsfl-ai (default: ../dsfl-ai); the
#                providers, services and BGT value definitions are read from there
#   PG*          database of the export (default: the docker-compose database on 127.0.0.1:5436)
#   PORTOLAN_PY  Python of the portolan-cli tool environment (`uv tool install portolan-cli==0.9.0`)
#   EXPORT_PY    Python with the GDAL bindings (osgeo) for export.py; default: python3 if it has
#                them, else the Python that Homebrew's gdal installed its bindings for
#                (<brew prefix>/lib/python3.X -> <brew prefix>/bin/python3.X, so it follows a
#                Homebrew upgrade to a new Python version)
#
# Steps: gen_sql.py (queries from the ldproxy providers) -> export.py (GeoParquet, Hilbert-sorted
# with gpio; needs GDAL with Python bindings) -> thumbnails.py -> build_catalog.py (metadata.yaml,
# portolan add, column descriptions, AGENTS.md with verified DuckDB recipes, READMEs, portolan
# check). Publishing (portolan push) is a separate step, see README.md.
set -e
cd "$(dirname "$0")/.."
DSFL_AI=${DSFL_AI:-../dsfl-ai}
PORTOLAN_PY=${PORTOLAN_PY:-$(uv tool dir)/portolan-cli/bin/python}
mkdir -p build
if [ "$1" != "--docs" ]; then
  if [ -z "$EXPORT_PY" ]; then
    BREW=$(brew --prefix 2>/dev/null || true)
    GDAL_PY=$(ls -d "$(brew --prefix gdal 2>/dev/null)"/lib/python3.* 2>/dev/null | sed "s|.*/lib/|$BREW/bin/|")
    for py in python3 $GDAL_PY; do
      if "$py" -c "from osgeo import ogr" 2>/dev/null; then EXPORT_PY=$py; break; fi
    done
  fi
  if [ -z "$EXPORT_PY" ]; then
    echo "no Python with the GDAL bindings (osgeo) found; set EXPORT_PY" >&2
    exit 1
  fi
  echo "export with $EXPORT_PY"
  python3 scripts/gen_sql.py "$DSFL_AI/entities/instances/providers" build/manifest.json
  "$EXPORT_PY" scripts/export.py build/manifest.json catalog
fi
"$PORTOLAN_PY" -I scripts/thumbnails.py build/manifest.json catalog
"$PORTOLAN_PY" -I scripts/build_catalog.py build/manifest.json catalog "$DSFL_AI"
