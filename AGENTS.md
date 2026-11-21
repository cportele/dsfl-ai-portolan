# Working on this repository

This file is for agents that change the catalog. Agents that only read the data start with
[catalog/AGENTS.md](catalog/AGENTS.md).

- `catalog/` is generated output. Never edit it by hand: change `scripts/` (texts in
  `agents_md.py` and `layout.py`, metadata in `build_catalog.py`, thumbnails in `thumbnails.py`)
  or the ldproxy configuration in the dsfl-ai repository, then run `scripts/build.sh --docs`.
- Claims about the data are measured, not typed: counts and value lists come from queries at build
  time, and a claim in the text gets a claim check (`Build.claim`, an HTML comment with a query
  for the rows that contradict it). A recipe that fails or returns no rows, or a claim check that
  returns rows, stops the build.
- Recipes use the published URLs (HTTPS, `s3://` for globs), so they can be copied as they are;
  the build runs them against the local files.
- Publishing uses `portolan push` and `catalog/versions.json`, not a separate upload script.
- Checks: `uvx rashid==0.4.0 check --all catalog` (no errors or warnings) and
  `uv run tests/check_docs.py catalog [--local catalog]`. Do not weaken a check to make it pass;
  fix the docs, or the data if it changed unintentionally.
