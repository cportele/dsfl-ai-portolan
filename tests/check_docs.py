# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb>=1.5"]
# ///
"""Run the documented queries and claim checks of the catalog against the published data.

Reads every AGENTS.md below the catalog directory:
- each ```sql block is run as it is, in a fresh DuckDB connection, and has to return rows; a block
  preceded by `<!-- check: fragment -->` is a fragment and is skipped;
- each `<!-- claim-check: <claim>` comment holds a query for the rows that contradict the claim;
  it has to return none.

  uv run tests/check_docs.py catalog                     # against the bucket (as published)
  uv run tests/check_docs.py catalog --local catalog     # against the local files of a build
  uv run tests/check_docs.py catalog --report out.md     # also write a Markdown report

Exit status 1 if a query fails, a recipe returns no rows or a claim does not hold.
"""

import argparse
import re
import sys
import time
from pathlib import Path

import duckdb

BUCKET = "dsfl-ai-417829795942-eu-central-1-an"
BUCKET_URL = f"https://{BUCKET}.s3.eu-central-1.amazonaws.com"
S3_URL = f"s3://{BUCKET}"

FENCE = re.compile(r"(?P<marker><!-- check: fragment -->\n)?```sql\n(?P<sql>.*?)\n```", re.S)
CLAIM = re.compile(r"<!-- claim-check: (?P<label>[^\n]*)\n(?P<sql>.*?)\n-->", re.S)


def blocks(path):
    text = path.read_text(encoding="utf-8")
    for m in FENCE.finditer(text):
        if not m.group("marker"):
            yield "recipe", text[: m.start()].count("\n") + 1, None, m.group("sql")
    for m in CLAIM.finditer(text):
        yield "claim", text[: m.start()].count("\n") + 1, m.group("label"), m.group("sql")


def run(sql, local):
    if local:
        sql = sql.replace(BUCKET_URL + "/", f"{local}/").replace(S3_URL + "/", f"{local}/")
        sql = re.sub(r"CREATE SECRET[^;]*;", "", sql)
    con = duckdb.connect()
    try:
        cur = con.execute(sql)
        return cur.fetchmany(3) if cur.description else []
    finally:
        con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catalog", type=Path)
    ap.add_argument("--local", type=Path, help="read the files from this directory instead of the bucket")
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    local = args.local.resolve() if args.local else None
    failures, count = [], 0
    for path in sorted(args.catalog.rglob("AGENTS.md")):
        rel = path.relative_to(args.catalog)
        for kind, line, label, sql in blocks(path):
            count += 1
            start = time.time()
            try:
                rows = run(sql, local)
                if kind == "recipe" and not rows:
                    problem = "returned no rows"
                elif kind == "claim" and rows:
                    problem = f"claim does not hold ({label}): {rows}"
                else:
                    problem = None
            except Exception as e:  # noqa: BLE001 - report every failure
                problem = f"failed: {str(e).splitlines()[0]}"
            status = "FAIL" if problem else "ok"
            print(f"{status:4} {rel}:{line} {kind} {time.time() - start:.1f}s" + (f" - {problem}" if problem else ""),
                  flush=True)
            if problem:
                failures.append((rel, line, kind, problem, sql))
    print(f"{count} checks, {len(failures)} failed")
    if args.report:
        lines = [f"{count} documented queries and claim checks, {len(failures)} failed.", ""]
        for rel, line, kind, problem, sql in failures:
            lines += [f"- `catalog/{rel}` line {line} ({kind}): {problem}", "", "  ```sql",
                      *("  " + x for x in sql.splitlines()), "  ```", ""]
        args.report.write_text("\n".join(lines) + "\n")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
