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
  python3 scripts/gen_sql.py "$DSFL_AI/entities/instances/providers" build/manifest.json
  python3 scripts/export.py build/manifest.json catalog
fi
"$PORTOLAN_PY" -I scripts/thumbnails.py build/manifest.json catalog
"$PORTOLAN_PY" -I scripts/build_catalog.py build/manifest.json catalog "$DSFL_AI"
