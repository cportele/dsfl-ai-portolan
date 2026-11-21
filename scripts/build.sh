#!/bin/sh
# Builds the Portolan catalog (GeoParquet + STAC) of the BAG, BGT, wijkenbuurten and postcode6
# data from the docker-compose database (127.0.0.1:5436, see export.py for PG* variables).
# Requires GDAL with the Parquet driver (Python bindings) and `uv tool install portolan-cli`.
#
#   scripts/portolan/build.sh [<output dir>]     default: tmp/portolan
#
# Steps: gen_sql.py (queries from the ldproxy providers) -> export.py (GeoParquet, Hilbert-sorted
# with gpio) -> build_catalog.py (metadata.yaml, portolan add, column descriptions, AGENTS.md with
# verified DuckDB recipes, portolan readme + check). Publishing (portolan push) is a separate step.
set -e
cd "$(dirname "$0")/../.."
OUT=${1:-tmp/portolan}
PORTOLAN_PY=${PORTOLAN_PY:-$HOME/.local/share/uv/tools/portolan-cli/bin/python}
mkdir -p "$OUT"
python3 scripts/portolan/gen_sql.py entities/instances/providers "$OUT/manifest.json"
python3 scripts/portolan/export.py "$OUT/manifest.json" "$OUT/catalog"
"$PORTOLAN_PY" -I scripts/portolan/build_catalog.py "$OUT/manifest.json" "$OUT/catalog" .
