#!/usr/bin/env python3
"""Turn the GeoParquet files of export.py into a Portolan catalog.

Run with the Python of the portolan-cli tool environment (it has duckdb, pyarrow and PyYAML):

  <portolan-cli python> -I build_catalog.py <manifest.json> <catalog dir> <dsfl-ai dir>

Steps:
1. portolan clean + init (always from scratch), .portolan/config.yaml
2. .portolan/metadata.yaml for the root, the four subcatalogs and every collection: titles,
   descriptions, licence, providers, source and attribution come from the API configuration
   (entities/instances/services/<api>.yml and the providers in the dsfl-ai checkout); the
   descriptions of the BGT groups get their example values from the data (layout.VALUES)
3. portolan add . --force (adopts the thumbnail.png of thumbnails.py), portolan logo
4. collection.json: column descriptions (from the provider, without the API-only sentences), the
   temporal extent, asset titles and descriptions, the bbox of the collections without geometry;
   `updated` on every catalog, vcs and issues links on the root
5. AGENTS.md for the root, the subcatalogs and the collections; every SQL recipe and claim check
   in them is run against the files first and the build stops if one fails
6. portolan readme, then the READMEs of the catalogs are completed (portolan-cli 0.9.0 writes
   broken collection links and no list of child catalogs), portolan check
"""

import json
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import duckdb
import yaml

sys.path.insert(0, str(Path(__file__).parent))  # run with python -I
from agents_md import BUCKET_URL, REPO_URL, S3_SECRET, S3_URL  # noqa: E402
from layout import GROUPS, VALUES, rel_dir  # noqa: E402

APIS = {
    "bag": {
        "short": "BAG",
        "source_url": "https://www.kadaster.nl/zakelijk/producten/adressen-en-gebouwen/bag-2.0-extract",
        "spdx": "CC0-1.0",
        "loader": "scripts/load_bag.py, scripts/finalize.sql",
    },
    "bgt": {
        "short": "BGT",
        "source_url": "https://www.pdok.nl/introductie/-/article/basisregistratie-grootschalige-topografie-bgt-",
        "spdx": "CC0-1.0",
        "loader": "scripts/load_bgt.py",
    },
    "wijkenbuurten": {
        "short": "CBS",
        "source_url": "https://api.pdok.nl/cbs/wijken-en-buurten-2026/ogc/v1",
        "spdx": "CC-BY-4.0",
        "loader": "scripts/load_gebieden.sh, scripts/gebieden.sql",
    },
    "postcode6": {
        "short": "CBS",
        "source_url": "https://www.pdok.nl/introductie/-/article/cbspostcode6",
        "spdx": "CC-BY-4.0",
        "loader": "scripts/load_postcode6.sh, scripts/postcode6.sql",
    },
}

API_BASE = "https://bag.ldproxy.net"
DSFL_AI_URL = "https://github.com/cportele/dsfl-ai"
LOGO = Path(__file__).parent.parent / "assets/logo.png"
SKILL_URL = "https://github.com/cportele/dsfl-ai/tree/master/skills/dsfl-ai-gebouwde-omgeving"

# Which version of an object is the current one; the same rule as the APIs without `datetime`.
CURRENT = {
    "bag": "beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)",
    "bgt": "eindRegistratie IS NULL",
}

# Sentences or clauses of the provider descriptions that only apply to the API.
DROP = re.compile(
    r"standaard niet in de uitvoer|Filter hierop alleen samen|Wordt als link met rel|"
    r"staat daarom niet in de uitvoer|parameter `datetime`|^met `datetime=|"
    r"titel (van|bij) de verwijzing|Als filter volstaat|^filter op de naam|"
    r"Voor de adressen zelf|zoekt men met een filter|de link leidt dan niet|"
    r"in de API en wordt alleen|eindigt de titel",
)
# Sentences of the API descriptions that only apply to the API server.
API_ONLY = re.compile(r"Deze server|Gaat een vraag|/collections/|/items\b")
REF = re.compile(
    r"(, )?[Ee]en verwijzing naar [^:]*?\(/[^)]*\)[^:]*: de link naar het object[^.;]*"
)


def clean(text, ref_note=None):
    if not text:
        return ref_note
    text = REF.sub("", text)
    text = text.replace(" en staat daarom niet bij de eigenschappen", "")
    text = text.replace(", om op te filteren", "")
    # national usage notes that do not hold for this extract
    text = text.replace("De waarde 9999 komt veel voor en betekent", "De waarde 9999 betekent")
    text = re.sub(r"\bin deze API\b", "in deze gegevens", text)
    text = re.sub(r"\bvan het record in deze gegevens\b", "van het record", text)
    clauses = [c for c in re.split(r"(?<=[.;])\s+", text.strip()) if c and not DROP.search(c)]
    out = " ".join(c for c in clauses if c not in (".", ";"))
    out = re.sub(r"[;,]\s*$", ".", out.strip())
    if out and not out.endswith("."):
        out += "."
    if ref_note:
        out = (out + " " + ref_note).strip()
    return out or None


def first_paragraph(text):
    return text.strip().split("\n\n")[0].strip()


def without_api_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text.strip())
    return " ".join(x for x in sentences if not API_ONLY.search(x))


def first_sentence(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text or "")  # links -> text
    return re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text.strip())[0]


def run(cmd, cwd):
    print("$", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(textwrap.indent(out[-4000:], "  "), flush=True)
    return r.returncode


def portolan():
    return shutil.which("portolan") or str(Path.home() / ".local/bin/portolan")


def write_yaml(path, data, header):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# {header}\n# generated by scripts/build_catalog.py - do not edit\n"
        + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)
    )


class Build:
    def __init__(self, manifest, catalog, repo):
        self.types = json.loads(Path(manifest).read_text())
        self.catalog = Path(catalog).resolve()
        self.repo = Path(repo).resolve()
        self.services = {
            api: yaml.safe_load((self.repo / f"entities/instances/services/{api}.yml").read_text())
            for api in APIS
        }
        # type -> id column, for the reference notes
        self.id_column = {}
        for t in self.types:
            ids = [c["name"] for c in t["columns"] if c["role"] == "ID"]
            self.id_column[(t["api"], t["type"])] = ids[0] if ids else "identificatie"
        self.apis = APIS
        self.db = duckdb.connect()
        self.db.sql("LOAD spatial")
        self.db.sql("SET geometry_always_xy = true")

    # ---------- helpers

    def parquet(self, t):
        return self.catalog / rel_dir(t["api"], t["type"]) / f"{t['type']}.parquet"

    def ref_target(self, t, col):
        """(api, type) a FEATURE_REF column points to."""
        key = (col.get("refApi"), col["refType"])
        return key if key in self.id_column else None

    def local(self, sql):
        """A recipe on the published files, rewritten for the local files of the build."""
        sql = sql.replace(S3_SECRET, "").replace("INSTALL spatial;", "")
        return sql.replace(BUCKET_URL + "/", f"{self.catalog}/").replace(S3_URL + "/", f"{self.catalog}/")

    def sql_ok(self, sql, cwd):
        """Run a recipe with the directory of its AGENTS.md as working directory."""
        self.db.sql(f"SET file_search_path = '{cwd}'")
        try:
            res = self.db.sql(self.local(sql)).fetchmany(3)
        except Exception as e:
            sys.exit(f"recipe failed in {cwd}:\n{sql}\n{e}")
        if not res:
            sys.exit(f"recipe returned no rows in {cwd}:\n{sql}")
        return res

    def has_rows(self, sql, cwd):
        self.db.sql(f"SET file_search_path = '{cwd}'")
        try:
            return bool(self.db.sql(self.local(textwrap.dedent(sql))).fetchmany(1))
        except Exception:
            return False

    def recipe(self, title, sql, cwd):
        sql = textwrap.dedent(sql).strip()
        self.sql_ok(sql, cwd)
        return f"{title}\n\n```sql\n{sql}\n```\n"

    def claim(self, label, sql):
        """A claim check: a query for the rows that contradict a claim of the text. It has to
        return none; it is published as an HTML comment, which tests/check_docs.py runs."""
        sql = textwrap.dedent(sql).strip()
        try:
            rows = self.db.sql(self.local(sql)).fetchmany(3)
        except Exception as e:
            sys.exit(f"claim check failed: {label}\n{sql}\n{e}")
        if rows:
            sys.exit(f"claim does not hold: {label}\n{sql}\n{rows}")
        return f"<!-- claim-check: {label}\n{sql}\n-->\n"

    def values(self, typ, column, k=4):
        """The most frequent values of a column of a BGT collection (current versions, else all)."""
        t = next(t for t in self.types if t["type"] == typ and t["api"] == "bgt")
        f = self.parquet(t)
        cond = "eindRegistratie IS NULL"
        if not self.db.sql(f"SELECT count(*) FROM '{f}' WHERE {cond}").fetchone()[0]:
            cond = "true"
        rows = self.db.sql(
            f"SELECT {column}, count(*) FROM '{f}' WHERE {cond} AND {column} IS NOT NULL "
            f"AND {column} NOT IN ('waardeOnbekend', 'geenWaarde') GROUP BY ALL ORDER BY 2 DESC, 1"
        ).fetchall()
        shown = ", ".join(f"'{r[0]}'" for r in rows[:k])
        return shown + (" enzovoort" if len(rows) > k else "")

    def scope(self, api):
        """What the extract of a registry holds, from the data."""
        if api == "bag":
            t = next(t for t in self.types if t["api"] == "bag" and t["type"] == "woonplaats")
            names = [r[0] for r in self.db.sql(
                f"SELECT naam FROM '{self.parquet(t)}' WHERE {CURRENT['bag']} ORDER BY naam").fetchall()]
            return (
                "Het uittreksel bevat de BAG van de gemeente Amersfoort, met de woonplaatsen "
                + ", ".join(names[:-1]) + f" en {names[-1]}."
            )
        if api == "wijkenbuurten":
            counts = {}
            names = []
            for typ in ("gemeente", "wijk", "buurt"):
                t = next(t for t in self.types if t["api"] == api and t["type"] == typ)
                counts[typ] = self.db.sql(f"SELECT count(*) FROM '{self.parquet(t)}'").fetchone()[0]
                if typ == "gemeente":
                    names = [r[0] for r in self.db.sql(
                        f"SELECT naam FROM '{self.parquet(t)}' ORDER BY naam").fetchall()]
            return (
                f"Het uittreksel bevat de gemeente {', '.join(names)} met {counts['wijk']} wijken en "
                f"{counts['buurt']} buurten."
            )
        if api == "postcode6":
            from agents_md import postcode6_scope

            return postcode6_scope(self, claims=False).strip()
        return ""

    # ---------- metadata.yaml

    def metadata(self):
        root_meta = self.services["bag"]["metadata"]
        write_yaml(
            self.catalog / ".portolan/metadata.yaml",
            {
                "title": "Amersfoort: BAG, BGT en CBS-gebieden (DSFL AI)",
                "description": (
                    "De gegevens achter de OGC API's op "
                    f"[bag.ldproxy.net]({API_BASE}) als GeoParquet, met historie: de Basisregistratie "
                    "Adressen en Gebouwen (BAG) voor de gemeente Amersfoort en de Basisregistratie "
                    "Grootschalige Topografie (BGT) voor de omgeving van Amersfoort, met de gemeenten, wijken en buurten en de "
                    "postcodegebieden van het CBS. Een collectie per objecttype van de API's, met "
                    "dezelfde eigenschappen. Voor agents: [AGENTS.md](AGENTS.md). Elke API is ook "
                    "een MCP-server; voor agents die die gebruiken is er de skill "
                    f"[dsfl-ai-gebouwde-omgeving]({SKILL_URL})."
                ),
                "contact": {"name": root_meta["contactName"], "email": root_meta["contactEmail"]},
                "license": "CC-BY-4.0",
                "keywords": ["BAG", "BGT", "CBS", "Amersfoort", "adressen", "gebouwen", "topografie"],
            },
            "catalog root",
        )
        for api, conf in APIS.items():
            svc = self.services[api]
            meta = svc["metadata"]
            write_yaml(
                self.catalog / api / ".portolan/metadata.yaml",
                {
                    "title": svc["label"],
                    "description": " ".join(
                        x for x in [without_api_sentences(first_paragraph(svc["description"])),
                                    self.scope(api)] if x
                    )
                    + f"\n\nDe gegevens van de API [{API_BASE}/{api}]({API_BASE}/{api}) als GeoParquet. "
                    "Voor agents: [AGENTS.md](AGENTS.md).",
                    "contact": {"name": meta["contactName"], "email": meta["contactEmail"]},
                    "license": conf["spdx"],
                    "license_url": meta["licenseUrl"],
                    "providers": [
                        {
                            "name": meta["creatorName"],
                            "roles": ["producer", "licensor"],
                            "url": meta["creatorUrl"],
                        },
                        {
                            "name": meta["publisherName"],
                            "roles": ["processor", "host"],
                            "url": meta["publisherUrl"],
                        },
                    ],
                    "source_url": conf["source_url"],
                    "attribution": meta["attribution"],
                    "keywords": meta.get("keywords", []),
                    "processing_notes": (
                        f"Geladen in PostgreSQL/PostGIS met de scripts van de repository dsfl-ai "
                        f"({DSFL_AI_URL}; {conf['loader']}), de database achter de API "
                        f"{API_BASE}/{api}. Per objecttype geëxporteerd met de scripts van {REPO_URL}: "
                        "gen_sql.py leidt de queries af "
                        "uit de feature provider van ldproxy, zodat de kolommen de eigenschappen van "
                        "de API zijn; export.py schrijft de bestanden met GDAL en sorteert ze met gpio "
                        "langs een Hilbert-curve (GeoParquet 2.0). Bogen zijn benaderd door "
                        "lijnstukken met een maximale afwijking van 1 mm. Kolommen met verwijzingen "
                        "bevatten alleen de identificatie."
                    ),
                },
                f"subcatalog {api}",
            )
            for group, gconf in GROUPS.get(api, {}).items():
                write_yaml(
                    self.catalog / api / group / ".portolan/metadata.yaml",
                    {
                        "title": gconf["title"],
                        "description": self.group_description(api, group)
                        + " Voor agents: [AGENTS.md](AGENTS.md).",
                    },
                    f"subcatalog {api}/{group}",
                )
        for t in self.types:
            short = APIS[t["api"]]["short"]
            versions = {
                "bag": "Met historie: een rij per voorkomen (versie) van een object, sleutel "
                "identificatie en voorkomenidentificatie.",
                "bgt": "Met historie: een rij per versie van een object, sleutel identificatie en "
                "tijdstipRegistratie; de versies die nu in de registratie staan hebben geen "
                "eindRegistratie.",
            }.get(t["api"], "")
            write_yaml(
                self.parquet(t).parent / ".portolan/metadata.yaml",
                {
                    "title": f"{t['label']} ({short})",
                    "description": " ".join(
                        x
                        for x in [
                            clean(t["description"]),
                            versions,
                            f"Dezelfde eigenschappen als de collectie [{t['type']}]"
                            f"({API_BASE}/{t['api']}/collections/{t['type']}) van de API. "
                            "Voor agents: [AGENTS.md](AGENTS.md).",
                        ]
                        if x
                    ),
                },
                f"collection {t['api']}/{t['type']}",
            )

    def group_description(self, api, group):
        return VALUES.sub(lambda m: self.values(m.group(1), m.group(2)), GROUPS[api][group]["description"])

    # ---------- collection.json

    def columns_and_extent(self):
        for t in self.types:
            path = self.parquet(t).parent / "collection.json"
            coll = json.loads(path.read_text())
            by_name = {c["name"]: c for c in t["columns"]}
            for col in coll.get("table:columns", []):
                c = by_name.get(col["name"])
                if c is None:
                    if col["name"].endswith("_bbox"):
                        col["description"] = (
                            f"Bounding box van {col['name'][:-5]} (GeoParquet covering), om bij een "
                            "ruimtelijke selectie rijgroepen over te slaan."
                        )
                    continue
                note = None
                if c["featureRef"]:
                    target = self.ref_target(t, c)
                    if target:
                        note = (
                            f"Verwijst naar {self.id_column[target]} in de collectie "
                            f"{rel_dir(*target).as_posix()}."
                        )
                desc = clean(c["description"], note) or c["label"]
                if desc:
                    col["description"] = desc
            start = self.temporal_start(t)
            if start:
                coll.setdefault("extent", {})["temporal"] = {"interval": [[start, None]]}
            path.write_text(json.dumps(coll, ensure_ascii=False, indent=2) + "\n")

    def temporal_start(self, t):
        f = self.parquet(t)
        names = {c["name"] for c in t["columns"]}
        if t["api"] == "bag" and "beginGeldigheid" in names:
            v = self.db.sql(f"SELECT min(beginGeldigheid) FROM '{f}'").fetchone()[0]
        elif t["api"] == "bgt":
            v = self.db.sql(f"SELECT min(objectBeginTijd) FROM '{f}'").fetchone()[0]
        elif t["api"] == "wijkenbuurten":
            return "2026-01-01T00:00:00Z"
        elif t["api"] == "postcode6":
            return "2024-01-01T00:00:00Z"
        else:
            return None
        return f"{v.isoformat()}T00:00:00Z" if v else None

    def post_stac(self):
        """What `portolan add` leaves out: asset titles and descriptions, a bbox for the
        collections without geometry, `updated` on every catalog, vcs and issues links."""
        bbox = {}
        for t in self.types:
            if t["geometries"]:
                coll = json.loads((self.parquet(t).parent / "collection.json").read_text())
                b = coll["extent"]["spatial"]["bbox"][0]
                old = bbox.get(t["api"], b)
                bbox[t["api"]] = [min(old[0], b[0]), min(old[1], b[1]), max(old[2], b[2]), max(old[3], b[3])]
        for t in self.types:
            path = self.parquet(t).parent / "collection.json"
            coll = json.loads(path.read_text())
            short = APIS[t["api"]]["short"]
            geo = bool(t["geometries"])
            for key, asset in coll.get("assets", {}).items():
                roles = asset.get("roles", [])
                if "thumbnail" in roles:
                    asset["title"] = f"Voorbeeld: {t['label']} ({short})"
                    asset["description"] = (
                        "Kaartje van de actuele versies (of van alle versies als er geen actuele zijn), "
                        "gekleurd naar de classificatie; gemaakt met scripts/thumbnails.py."
                    )
                elif "data" in roles or asset.get("href", "").endswith(".parquet"):
                    asset["title"] = f"{t['label']} ({short}), " + ("GeoParquet" if geo else "Parquet")
                    asset["description"] = (
                        "Alle versies van de objecten, met de eigenschappen van de API als kolommen. "
                        + ("GeoParquet 2.0, EPSG:28992, rijen gesorteerd langs een Hilbert-curve."
                           if geo else "Zonder geometrie, gesorteerd op identificatie en versie.")
                    )
            if not geo and t["api"] in bbox:
                # no geometry: the extent of the registry's collections with geometry
                coll["extent"]["spatial"]["bbox"] = [bbox[t["api"]]]
            path.write_text(json.dumps(coll, ensure_ascii=False, indent=2) + "\n")
        root = json.loads((self.catalog / "catalog.json").read_text())
        updated = root.get("updated")
        for path in self.catalog.rglob("catalog.json"):
            cat = json.loads(path.read_text())
            if updated:
                cat["updated"] = updated
            if path.parent == self.catalog:
                cat["links"] = [x for x in cat["links"] if x["rel"] not in ("vcs", "issues")] + [
                    {"rel": "vcs", "href": REPO_URL, "type": "text/html",
                     "title": "Repository met de scripts van deze catalogus"},
                    {"rel": "issues", "href": f"{REPO_URL}/issues", "type": "text/html",
                     "title": "Fouten en vragen"},
                ]
            path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + "\n")

    # ---------- README.md

    def readmes(self):
        """Complete the READMEs of `portolan readme`."""
        for path in self.catalog.rglob("catalog.json"):
            self.catalog_readme(path.parent)
        for t in self.types:
            readme = self.parquet(t).parent / "README.md"
            text = readme.read_text()
            text = re.sub(
                r'read_parquet\("\./([\w-]+\.parquet)"\)',
                lambda m: f'read_parquet("{BUCKET_URL}/{rel_dir(t["api"], t["type"]).as_posix()}/{m.group(1)}")',
                text,
            )
            if not t["geometries"]:  # plain Parquet: geopandas needs a geometry column
                text = text.replace("import geopandas as gpd", "import pandas as pd")
                text = text.replace("gdf = gpd.read_parquet(", "df = pd.read_parquet(")
                text = text.replace("print(gdf.head())", "print(df.head())")
            readme.write_text(text)

    def catalog_readme(self, directory):
        readme = directory / "README.md"
        text = readme.read_text()
        cat = json.loads((directory / "catalog.json").read_text())
        children, collections = [], []
        for link in cat["links"]:
            if link["rel"] != "child":
                continue
            target = (directory / link["href"]).resolve()
            data = json.loads(target.read_text())
            entry = (target.parent.relative_to(directory).as_posix(), data)
            (collections if data.get("type") == "Collection" else children).append(entry)
        sections = []
        if children:
            rows = ["| Catalogus | Inhoud | Collecties | Licentie |", "|---|---|---|---|"]
            for rel, data in children:
                n = sum(1 for _ in (directory / rel).rglob("collection.json"))
                lic = sorted({json.loads(p.read_text()).get("license", "")
                              for p in (directory / rel).rglob("collection.json")})
                rows.append(f"| [{data.get('title', rel)}]({rel}/README.md) | "
                            f"{first_sentence(data.get('description'))} | {n} | {', '.join(lic)} |")
            sections.append("## Catalogs\n\n" + "\n".join(rows) + "\n")
        if collections:
            rows = ["| Collectie | Beschrijving |", "|---|---|"]
            for rel, data in sorted(collections, key=lambda x: x[0]):
                rows.append(f"| [{data.get('title', rel)}]({rel}/README.md) | "
                            f"{first_sentence(data.get('description'))} |")
            sections.append("## Collections\n\n" + "\n".join(rows) + "\n")
        block = "\n".join(sections)
        if "## Collections" in text:
            text = re.sub(r"## Collections\n.*?(?=\n## )", lambda m: block, text, flags=re.S)
        elif block:
            i = text.index("\n## ")
            text = text[: i + 1] + block + text[i:]
        if directory == self.catalog:
            licences = "\n".join(
                f"- {self.services[api]['label']}: "
                f"[{conf['spdx']}]({self.services[api]['metadata']['licenseUrl']})"
                + (f", {self.services[api]['metadata']['attribution']}" if conf["spdx"] != "CC0-1.0" else "")
                for api, conf in APIS.items()
            )
            text = re.sub(
                r"## License\n\n.*?(?=\n## |\n---)",
                lambda m: "## License\n\nDe licentie verschilt per registratie:\n\n" + licences + "\n",
                text, flags=re.S,
            )
            text = text.replace(
                "## Contact",
                f"## Source code\n\nDe scripts van deze catalogus: [{REPO_URL}]({REPO_URL}); fouten en "
                f"vragen: [{REPO_URL}/issues]({REPO_URL}/issues).\n\n## Contact",
                1,
            )
        readme.write_text(text)

    # ---------- AGENTS.md

    def agents(self):
        from agents_md import collection_md, group_md, root_md, subcatalog_md

        (self.catalog / "AGENTS.md").write_text(root_md(self))
        for api in APIS:
            (self.catalog / api / "AGENTS.md").write_text(subcatalog_md(self, api))
            for group in GROUPS.get(api, {}):
                (self.catalog / api / group / "AGENTS.md").write_text(group_md(self, api, group))
        for t in self.types:
            (self.parquet(t).parent / "AGENTS.md").write_text(collection_md(self, t))

    # ---------- main

    def run(self):
        p = portolan()
        # Always from scratch: a second `portolan add --force` fails on tabular collections with
        # a source_url (portolan-cli 0.9.0, pystac "Relative path ... without owner self link").
        if (self.catalog / "catalog.json").exists():
            run([p, "clean"], self.catalog)
        run([p, "init", "--auto", "--license", "CC-BY-4.0", "--id", "dsfl-ai-amersfoort"], self.catalog)
        cfg = self.catalog / ".portolan/config.yaml"
        cfg.write_text(
            "# generated by scripts/build_catalog.py - do not edit\n"
            "tabular:\n  enabled: true\n"
            "# thumbnail.png of scripts/thumbnails.py is adopted, nothing is rendered\n"
            "thumbnails:\n  enabled: true\n"
        )
        self.metadata()
        if run([p, "add", ".", "--force"], self.catalog):
            sys.exit("portolan add failed")
        if run([p, "logo", str(LOGO), "--title", "DSFL AI Amersfoort"], self.catalog):
            sys.exit("portolan logo failed")
        self.columns_and_extent()
        self.post_stac()
        self.agents()
        run([p, "readme"], self.catalog)
        self.readmes()
        if run([p, "check", "."], self.catalog):
            sys.exit("portolan check failed")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    Build(*sys.argv[1:4]).run()
