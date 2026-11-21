# dsfl-ai-portolan

The [Portolan](https://www.portolan-sdi.org/) catalog of the data behind the OGC APIs of the
[DSFL AI](https://github.com/cportele/dsfl-ai) project on [bag.ldproxy.net](https://bag.ldproxy.net):
the BAG of the gemeente Amersfoort and the BGT of the Amersfoort area, both with their full history,
and the CBS wijken en buurten 2026 and postcodegebieden (PC6) 2024, as GeoParquet.

- Catalog: <https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/catalog.json>
  (start with its [README](catalog/README.md) or, for agents, [AGENTS.md](catalog/AGENTS.md); the
  texts of the catalog are in Dutch)
- Problems with the catalog or the data: [issues](https://github.com/cportele/dsfl-ai-portolan/issues)

## Layout

| Path | Content |
|---|---|
| `catalog/` | The published catalog: STAC JSON, README.md and AGENTS.md per node, thumbnails, logo, `versions.json` of `portolan push`. All generated; the parquet files are not in git. |
| `scripts/` | The generator: `gen_sql.py` → `export.py` → `thumbnails.py` → `build_catalog.py` (see `build.sh`) |
| `tests/check_docs.py` | Runs the documented queries and claim checks of the AGENTS.md files |
| `assets/logo.png` | The catalog logo (`scripts/logo.py`) |
| `.github/workflows/` | `ci.yml`: rashid and the documented queries on every pull request; `docs-check.yml`: weekly check of the published catalog, opens an issue on failure |

Everything under `catalog/` is generated. Change the scripts, not the output; the texts come
from `scripts/agents_md.py` and `scripts/layout.py`, the descriptions of collections and columns
from the ldproxy configuration in the dsfl-ai repository.

## Build

Requirements: a checkout of [dsfl-ai](https://github.com/cportele/dsfl-ai) next to this one (or
`DSFL_AI=<path>`), `uv tool install portolan-cli==0.9.0`, and for the export the dsfl-ai database
(docker compose, 127.0.0.1:5436) and GDAL with Python bindings.

```sh
scripts/build.sh            # export from the database, thumbnails, metadata and docs
scripts/build.sh --docs     # only thumbnails, metadata and docs, from the existing parquet files
```

`build_catalog.py` runs every SQL recipe and claim check of the AGENTS.md files against the local
files and stops if one fails; `portolan check` runs at the end. Before publishing:

```sh
uvx rashid==0.4.0 check --all catalog
uv run tests/check_docs.py catalog --local catalog
```

## Publish

The catalog is published with `portolan push`, which tracks the uploads in `catalog/versions.json`
(commit it with the build):

```sh
cd catalog && portolan push s3://dsfl-ai-417829795942-eu-central-1-an --profile dsfl-ai
```

Pushing never deletes objects in the bucket. After a push, `uv run tests/check_docs.py catalog`
checks the documentation against the published data.

## Licence

The scripts and the texts of the catalog in this repository are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see [LICENSE](LICENSE). The data has the
licences of its sources (BAG and BGT CC0 1.0, CBS CC BY 4.0), listed in the
[catalog README](catalog/README.md).
