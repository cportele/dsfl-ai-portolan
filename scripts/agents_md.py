"""AGENTS.md texts of the Portolan catalog (used by build_catalog.py), in Dutch.

Every SQL recipe goes through Build.recipe, which runs it with DuckDB (spatial loaded) against
the files, with the directory of the AGENTS.md as working directory; a failing recipe stops the
build.
"""

import os
import re

from layout import GROUPS, rel_dir

API_BASE = "https://bag.ldproxy.net"
BUCKET = "dsfl-ai-417829795942-eu-central-1-an"
BUCKET_URL = f"https://{BUCKET}.s3.eu-central-1.amazonaws.com"
SKILL_URL = "https://github.com/cportele/dsfl-ai/tree/master/skills/dsfl-ai-gebouwde-omgeving"
# The value definitions per BGT collection are maintained with the skill (relative to the repo).
BGT_VALUES = "skills/dsfl-ai-gebouwde-omgeving/references/bgt-waarden/waarden-{typ}.md"

# "Woningen in gebruik", as in the skill: verblijfsobjecten with woonfunctie and these statuses.
IN_GEBRUIK = (
    "status IN ('Verblijfsobject in gebruik', 'Verblijfsobject in gebruik (niet ingemeten)', "
    "'Verbouwing verblijfsobject')"
)

API_AND_MCP = f"""\
## Dezelfde gegevens via de API's en MCP

De API's op {API_BASE} leveren dezelfde gegevens, met opgeslagen zoekopdrachten en een proces om te
tellen en op te tellen; elke API is ook een MCP-server (`{API_BASE}/<api>/mcp`). Voor agents die
de MCP-servers gebruiken is er een skill met de werkwijze en de valkuilen:
[dsfl-ai-gebouwde-omgeving]({SKILL_URL}). De valkuilen hieronder en in de AGENTS.md van de
subcatalogi komen daaruit, voor wie de bestanden zelf bevraagt.
"""

PITFALLS_ROOT = """\
## Wat een antwoord verandert

- **Een getal past bij de definitie die je noemt.** Een woning is in de BAG een verblijfsobject met
  gebruiksdoel woonfunctie; de bestanden bevatten alle statussen, ook in aanbouw, ingetrokken en
  gesloopt. Kies de statussen bewust en noem ze (zie de [AGENTS.md van de BAG](bag/AGENTS.md)).
- **Veranderingen zijn het verschil tussen twee toestanden**, met dezelfde definitie en hetzelfde
  gebied: de versies op de ene datum min de versies op de andere. Een telling op bouwjaar of op
  registratiedatum is iets anders.
- **Een geregistreerde gebeurtenis is niet altijd wat er gebeurd is**: 'Pand gesloopt' is ook een
  samenvoeging of een pand dat nooit is gebouwd; in de BGT zijn veel versies met hetzelfde
  tijdstip een bulkbewerking, geen verandering op straat.
- **Oppervlakte in een gebied: knippen.** Een object hoort bij de buurt (`buurtcode`) waarin een
  punt op zijn geometrie ligt; de oppervlakte binnen een buurt is de doorsnede met de grens uit
  `wijkenbuurten` (zie de [AGENTS.md van de BGT](bgt/AGENTS.md)).
- **Geregistreerd is niet aanwezig**: IMGeo-plus en de inrichtingselementen van de BGT zijn
  optioneel en vaak alleen door de provincie of het waterschap bijgehouden; een ontbrekende waarde
  van het CBS per postcode is 0 tot 4 of geheim, geen nul.
"""

COMMON = f"""\
## De bestanden lezen

- De paden in de voorbeelden zijn relatief ten opzichte van dit bestand. De catalogus staat
  openbaar in de S3-bucket `{BUCKET}` (eu-central-1):
  - via HTTPS: `{BUCKET_URL}/<pad>`, bijvoorbeeld
    `{BUCKET_URL}/bag/pand/pand.parquet`; DuckDB (`LOAD httpfs`) leest dan met
    range-requests alleen de rijgroepen en kolommen die nodig zijn;
  - via S3: `s3://{BUCKET}/<pad>`, zonder inloggegevens. Wildcards in paden
    (`read_parquet('s3://{BUCKET}/bgt/topografie/*/*.parquet')`) werken alleen zo, niet via HTTPS;
    in DuckDB eerst `CREATE SECRET (TYPE s3, REGION 'eu-central-1');`.
- GeoParquet 2.0: geometrieën als WKB met het Parquet-type GEOMETRY, in het Rijksdriehoeksstelsel
  (EPSG:28992, Amersfoort / RD New, in meter, x = oost, y = noord). Met de spatial-extensie van
  DuckDB heeft een geometriekolom het type GEOMETRY. Voor lengte- en breedtegraad:
  `ST_Transform(geometrie, 'EPSG:28992', 'OGC:CRS84')`.
- Elke rijgroep heeft ruimtelijke statistieken per geometriekolom, en elke geometriekolom heeft
  daarnaast een kolom `<naam>_bbox` (struct xmin, ymin, xmax, ymax). Filter eerst op de bounding
  box en pas daarna met een exact ruimtelijk predicaat, zodat lezers rijgroepen kunnen overslaan.
  De rijen zijn gesorteerd langs een Hilbert-curve van de primaire geometrie, in rijgroepen van
  49.152 rijen.
- Bogen in de BGT zijn benaderd door lijnstukken (maximale afwijking 1 mm); de afgeleide
  oppervlakten en lengten (`oppervlakte`, `lengte`) zijn uit de bogen berekend.
- Verwijzingen naar andere objecten bevatten alleen de identificatie. Eigenschappen en
  verwijzingen met meerdere waarden zijn Parquet-lijsten (`list_contains`, `unnest`); lijsten van
  objecten zijn JSON-tekst (`->>`, `json_extract`), met geometrieën daarin als GeoJSON in
  RD-coördinaten.
- Tijdstippen hebben geen tijdzone. In de BGT zijn het lokale tijden (Europe/Amsterdam), zoals de
  beschrijvingen van de kolommen vermelden.
"""

VERSIONS = {
    "bag": """\
## Versies (BAG)

Elke rij is een voorkomen (versie) van een object, met als sleutel `identificatie` +
`voorkomenidentificatie`. De versies van een object sluiten naadloos op elkaar aan, van
`beginGeldigheid` (inclusief) tot `eindGeldigheid` (exclusief, leeg bij de laatste versie). Versies
die op dezelfde dag weer zijn vervangen en inactieve of niet-BAG-voorkomens zijn niet opgenomen,
net als in de API. De versie die vandaag geldig is, zoals de API die zonder `datetime` levert:

```sql
WHERE beginGeldigheid <= current_date
  AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
```

Vervang `current_date` door een datum voor de versie die op die datum geldig was. Objecten die
niet meer bestaan (bijvoorbeeld `status = 'Pand gesloopt'` of `'Verblijfsobject ingetrokken'`)
hebben een geldige laatste versie met die eindstatus; filter op `status` om alleen bestaande
objecten te krijgen.
""",
    "bgt": """\
## Versies (BGT)

Elke rij is een versie van een object, met als sleutel `identificatie` + `tijdstipRegistratie`. De
versies van een object sluiten naadloos op elkaar aan, van `tijdstipRegistratie` (inclusief) tot
`eindRegistratie` (exclusief). De versies die nu in de registratie staan, zoals de API die zonder
`datetime` levert (alleen bestaande objecten):

```sql
WHERE eindRegistratie IS NULL
```

Op een tijdstip `T`: `tijdstipRegistratie <= T AND (eindRegistratie IS NULL OR eindRegistratie > T)`.
Een beëindigd object houdt zijn laatste versie, met `eindRegistratie` gelijk aan `objectEindTijd`.
""",
}

PITFALLS = {
    "bag": f"""\
## Wat een antwoord verandert (BAG)

- **Status**: de bestanden bevatten alle statussen. Woningen in gebruik zijn verblijfsobjecten met
  `list_contains(gebruiksdoel, 'woonfunctie')` en
  `{IN_GEBRUIK}`. Noem woningen in aanbouw ('Verblijfsobject gevormd') apart als ze ertoe doen.
  Panden: Bouwvergunning verleend, Bouw gestart, Pand in gebruik (niet ingemeten), Pand in gebruik,
  Verbouwing pand, Sloopvergunning verleend, Pand gesloopt, Pand buiten gebruik, Niet gerealiseerd
  pand, Pand ten onrechte opgevoerd.
- **Bouwjaar** (`oorspronkelijkBouwjaar`): 9999 is onbekend. Oude panden hebben vaak een geschat
  rond jaar (1600, 1700, 1800); aantallen per jaar vóór ongeveer 1900 zijn grof. `bouwjaarPand` bij
  een verblijfsobject is het oudste bouwjaar van zijn panden, `statusPand` de status van dat pand.
- **Oppervlakte** van een verblijfsobject is de gebruiksoppervlakte; 999999 is geen werkelijke
  oppervlakte. `grondoppervlakte` van een pand is berekend uit de geometrie; `>= 50` sluit schuren en
  garages uit.
- **Gebruiksdoel** is de vergunde gebruiksfunctie (Bouwbesluit 2012), geen soort voorziening
  (sportfunctie omvat ook kantines). Een verblijfsobject met meer gebruiksdoelen telt in een
  groepering op gebruiksdoel in elke groep mee.
- **Veranderingen**: de toestand op de ene datum min die op de andere. Woningen "gebouwd sinds" een
  jaar (`bouwjaarPand`) zijn niet de woningen die erbij zijn gekomen; in oude stadsdelen ontstaan de
  meeste in bestaande panden. Zie het voorbeeld hieronder.
- **'Pand gesloopt'** beëindigt ook een samenvoeging met een buurpand (dat op dezelfde datum groter
  wordt en de verblijfsobjecten overneemt) en een pand dat nooit is gebouwd. Zeg "als gesloopt
  geregistreerd", splits op grootte en controleer de grotere panden (voorbeeld hieronder).
- **`beginGeldigheid`** is de datum van de registratie, soms jaren na de gebeurtenis.
- **Woonboten en woonwagens** (`ligplaats`, `standplaats`) zijn geen verblijfsobjecten en ontbreken in
  elke telling van woningen; tel ze apart ('Plaats aangewezen').
- **Niet in de BAG**: bewoners (zie `postcode6`), bedrijven, eigenaren, prijzen, energielabels.
- **Gemeente, wijk en buurt** van een object zijn afgeleid uit de geometrie van elke versie; namen
  van wijken en buurten zijn alleen binnen een gemeente uniek.
""",
    "bgt": """\
## Wat een antwoord verandert (BGT)

- **De historie begint per bronhouder bij de eerste levering**, voor de meeste bronhouders eind
  2016, toen de BGT compleet werd; oudere `objectBeginTijd` zijn objecten die toen al bestonden.
  Vergelijk niet met een datum daarvoor; een toename tussen twee datums kan ook fijnere inwinning
  zijn.
- **Bulkbewerkingen**: honderden versies van één bronhouder met hetzelfde `tijdstipRegistratie` zijn
  een correctie of herinwinning, geen verandering op straat. De BGT onderscheidt een wijziging in de
  werkelijkheid niet van een correctie.
- **Wijzigingen in een periode**: nieuwe en gewijzigde objecten hebben een versie met
  `tijdstipRegistratie` in de periode, beëindigde objecten een laatste versie
  (`volgendeVersie IS NULL`) met `eindRegistratie` in de periode. Wie alleen op
  `tijdstipRegistratie` filtert, mist de beëindigde objecten.
- **Maaiveld**: alleen de vlakken met `relatieveHoogteligging = 0` bedekken het gebied zonder gaten
  en overlap; bruggen en overkappingen (1 en hoger), tunnels (-1 en lager) en functionele gebieden
  (parken, speeltuinen) liggen erboven, eronder of overlappen ze.
- **Oppervlakte in een gebied**: een object hoort bij de buurt (`buurtcode`) waarin een punt op zijn
  geometrie ligt, ook als het over de grens loopt. Voor water en grote wegen kan dat tientallen
  procenten schelen; knip daarom met de grens uit `wijkenbuurten` (voorbeeld hieronder). Het totaal
  voor een aandeel is de som van de geknipte vlakken op maaiveld.
- **Groen en erf**: `begroeidterreindeel` is het groen; `onbegroeidterreindeel` met
  `bgtFysiekVoorkomen = 'erf'` is de grond bij een pand (tuinen, binnenplaatsen, opritten). Een
  aandeel groen bevat dus geen tuinen; noem het aandeel erf erbij.
- **IMGeo-plus en inrichtingselementen** (bomen, banken, lichtmasten, putten, speeltoestellen) zijn
  optioneel en alleen gevuld waar de bronhouder ze bijhoudt. Groepeer eerst op `bronhouder` (G...
  gemeente, P... provincie, W... waterschap, L... Rijk) en zeg "in de BGT geregistreerd" en door wie.
  `plusFysiekVoorkomen = 'waardeOnbekend'` kan een groot deel van de wegoppervlakte zijn;
  `bgtFysiekVoorkomen` is volledig.
- **Waarden**: een waarde met een dubbele punt verfijnt de waarde ervoor (`'recreatie: speeltuin'`
  is een soort `'recreatie'`; alle soorten met `LIKE 'recreatie%'`). `transitie` komt voor bij
  bgtFunctie en bgtType, maar staat in geen waardelijst. De definities van de waarden staan in de
  AGENTS.md van elke collectie.
""",
    "postcode6": """\
## Wat een antwoord verandert (postcode6)

- Aantallen zijn op vijftallen afgerond, percentages op tientallen. Het CBS publiceert een waarde
  alleen bij ten minste vijf inwoners, huishoudens of woningen (percentages bij ten minste tien):
  **een ontbrekende waarde is 0 tot 4 of geheim**, geen nul en geen onbekend aantal.
- **Sommen zijn ondergrenzen**, sommen van deelgroepen (leeftijdsklassen, huishoudtypen) nog meer;
  zeg "minstens" en hoeveel postcodes een waarde hebben (`count(kolom)` naast `count(*)`).
- **Percentages** en `gemiddelde_huishoudensgrootte` zijn niet op te tellen. Een gewogen gemiddelde
  telt alleen de postcodes met een waarde; `percentage_koopwoningen` en `percentage_huurwoningen`
  ontbreken zo vaak (vaak heeft een postcode er maar één van) dat er geen aandeel per wijk uit volgt.
- **Sorteren**: `ORDER BY ... DESC` zet in DuckDB de ontbrekende waarden achteraan, maar een
  vergelijking (`< 5`) treft een ontbrekende waarde nooit.
""",
}

CURRENT = {
    "bag": "beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)",
    "bgt": "eindRegistratie IS NULL",
}


def cur(api, alias=None):
    c = CURRENT.get(api)
    if not c:
        return "true"
    if alias:
        for col in ("beginGeldigheid", "eindGeldigheid", "eindRegistratie"):
            c = c.replace(col, f"{alias}.{col}")
    return c


def n(x):
    """Number with Dutch thousands separator."""
    return f"{x:,}".replace(",", ".")


def rel(b, frm, api, typ):
    """Path of the file of api/typ relative to the directory frm."""
    return os.path.relpath(b.catalog / rel_dir(api, typ) / f"{typ}.parquet", frm)


def geometry_names(b, api, typ):
    for t in b.types:
        if t["api"] == api and t["type"] == typ:
            return [g["name"] for g in t["geometries"]]
    return []


def collection_table(b, types, frm, with_group=False):
    head = "| Collectie | Rijen | Geometrie |\n|---|---|---|"
    if with_group:
        head = "| Collectie | Subcatalogus | Rijen | Geometrie |\n|---|---|---|---|"
    lines = [head]
    for t in types:
        rows = b.db.sql(f"SELECT count(*) FROM '{b.parquet(t)}'").fetchone()[0]
        geoms = ", ".join(g["name"] for g in t["geometries"]) or "geen"
        link = os.path.relpath(b.parquet(t).parent / "AGENTS.md", frm)
        cell = f"[`{t['type']}`]({link}) ({t['label']})"
        if with_group:
            group = rel_dir(t["api"], t["type"]).parent.name
            lines.append(f"| {cell} | `{group}` | {n(rows)} | {geoms} |")
        else:
            lines.append(f"| {cell} | {n(rows)} | {geoms} |")
    return "\n".join(lines) + "\n"


def root_md(b):
    cwd = b.catalog
    counts = {
        api: sum(1 for t in b.types if t["api"] == api)
        for api in ("bag", "bgt", "wijkenbuurten", "postcode6")
    }

    def p(api, typ):
        return rel(b, cwd, api, typ)

    parts = [
        f"""\
# Amersfoort: BAG, BGT en CBS-gebieden (DSFL AI)

De gegevens achter de OGC API's op {API_BASE} als GeoParquet: de BAG van de gemeente Amersfoort en
de BGT van de omgeving van Amersfoort, beide met de volledige historie, de gemeenten, wijken en
buurten 2026 van het CBS en de postcodegebieden (PC6) 2024 van het CBS. Een collectie per
objecttype van de API's, met de namen van de eigenschappen van de API als kolomnamen; de
beschrijvingen van de kolommen staan in elke `collection.json` (`table:columns`) en README.

| Subcatalogus | API | Collecties | Licentie |
|---|---|---|---|
| [`bag/`](bag/AGENTS.md) | {API_BASE}/bag | {counts['bag']} | CC0 1.0 |
| [`bgt/`](bgt/AGENTS.md) | {API_BASE}/bgt | {counts['bgt']} | CC0 1.0 |
| [`wijkenbuurten/`](wijkenbuurten/AGENTS.md) | {API_BASE}/wijkenbuurten | {counts['wijkenbuurten']} | CC BY 4.0 (CBS) |
| [`postcode6/`](postcode6/AGENTS.md) | {API_BASE}/postcode6 | {counts['postcode6']} | CC BY 4.0 (CBS, ESRI Nederland) |

Elke collectie is één bestand `<objecttype>.parquet` in een eigen map, met een eigen `AGENTS.md`.
De BGT is verdeeld in drie subcatalogi: `bgt/topografie`, `bgt/inrichtingselementen` en
`bgt/overig`. De AGENTS.md van de subcatalogi beschrijven de versies en de verwijzingen binnen een
registratie.

{API_AND_MCP}
{COMMON}
{PITFALLS_ROOT}
## Verwijzingen tussen de subcatalogi

- `gemeentecode`, `wijkcode` en `buurtcode` (BAG-panden, -verblijfsobjecten, -ligplaatsen en
  -standplaatsen, alle BGT-objecten, postcode6) = `code` van de collecties gemeente, wijk en buurt
  in `wijkenbuurten`. De codes zijn afgeleid uit de CBS Wijk- en Buurtkaart 2026, het zijn geen
  BAG- of BGT-gegevens. De buurtcode bevat ook de gemeentecode en de wijkcode: BU03070100 ligt in
  gemeente 0307, wijk WK030701.
- `nummeraanduiding.postcode` (BAG) = `postcode6.postcode`.
- `pand.identificatieBAGPND` (BGT) = `pand.identificatie` (BAG),
  `openbareruimtelabel.identificatieBAGOPR` (BGT) = `openbareruimte.identificatie` (BAG).

## Voorbeelden (DuckDB; `INSTALL spatial; LOAD spatial;` voor de geometriefuncties)
""",
        b.recipe(
            "De adressen van de verblijfsobjecten die vandaag geldig zijn in postcode 3811LM, met "
            "het aantal inwoners van het postcodegebied:",
            f"""
            SELECT o.naam AS straat, n.huisnummer, n.huisletter, n.huisnummertoevoeging, n.postcode,
                   v.identificatie AS verblijfsobject, p.aantal_inwoners AS inwoners_pc6
            FROM '{p('bag', 'verblijfsobject')}' v
            JOIN '{p('bag', 'nummeraanduiding')}' n
              ON n.identificatie = v.heeftAlsHoofdadres AND {cur('bag', 'n')}
            JOIN '{p('bag', 'openbareruimte')}' o
              ON o.identificatie = n.ligtAan AND {cur('bag', 'o')}
            LEFT JOIN '{p('postcode6', 'postcode6')}' p ON p.postcode = n.postcode
            WHERE {cur('bag', 'v')} AND n.postcode = '3811LM'
            ORDER BY n.huisnummer, n.huisletter, n.huisnummertoevoeging
            """,
            cwd,
        ),
        b.recipe(
            "Woningen in gebruik per wijk, met de naam van de wijk (verblijfsobjecten met "
            "woonfunctie, ook met andere gebruiksdoelen, met de statussen voor 'in gebruik'):",
            f"""
            SELECT w.code, w.naam, count(*) AS woningen
            FROM '{p('bag', 'verblijfsobject')}' v
            JOIN '{p('wijkenbuurten', 'wijk')}' w ON w.code = v.wijkcode
            WHERE {cur('bag', 'v')} AND list_contains(v.gebruiksdoel, 'woonfunctie')
              AND v.{IN_GEBRUIK}
            GROUP BY ALL ORDER BY woningen DESC
            """,
            cwd,
        ),
        b.recipe(
            "BGT-panden die nu in de registratie staan, met het oorspronkelijk bouwjaar uit de BAG:",
            f"""
            SELECT g.identificatie AS bgt_pand, g.identificatieBAGPND, b.oorspronkelijkBouwjaar
            FROM '{p('bgt', 'pand')}' g
            JOIN '{p('bag', 'pand')}' b
              ON b.identificatie = g.identificatieBAGPND AND {cur('bag', 'b')}
            WHERE {cur('bgt', 'g')}
            LIMIT 10
            """,
            cwd,
        ),
        b.recipe(
            "Ruimtelijke selectie: de BAG-panden die vandaag geldig zijn in een vierkant van 200 m bij "
            "de Onze Lieve Vrouwetoren (155000, 463000, de oorsprong van de RD-coördinaten), met het "
            "zwaartepunt in lengte- en breedtegraad (eerst het filter op de bounding box, dan het "
            "exacte predicaat):",
            f"""
            LOAD spatial;
            SELECT identificatie, oorspronkelijkBouwjaar,
                   ST_AsText(ST_Transform(ST_Centroid(geometrie), 'EPSG:28992', 'OGC:CRS84')) AS zwaartepunt
            FROM '{p('bag', 'pand')}'
            WHERE geometrie_bbox.xmax >= 155000 AND geometrie_bbox.xmin <= 155200
              AND geometrie_bbox.ymax >= 463000 AND geometrie_bbox.ymin <= 463200
              AND ST_Intersects(geometrie, ST_MakeEnvelope(155000, 463000, 155200, 463200))
              AND {cur('bag')}
            """,
            cwd,
        ),
    ]
    return "\n".join(parts)


def subcatalog_md(b, api):
    cwd = b.catalog / api

    def p(typ):
        return rel(b, cwd, api, typ)

    svc = b.services[api]
    types = [t for t in b.types if t["api"] == api]
    lines = [f"# {svc['label']}\n"]
    lines.append(
        f"De gegevens van de API {API_BASE}/{api} als GeoParquet, een collectie per objecttype; de "
        "kolomnamen zijn de namen van de eigenschappen van de API. Begin met de algemene "
        "aanwijzingen in de [AGENTS.md van de catalogus](../AGENTS.md).\n"
    )
    if api in GROUPS:
        lines.append(
            "De collecties zijn verdeeld in subcatalogi: "
            + ", ".join(f"[{c['title']}]({g}/AGENTS.md) (`{g}`)" for g, c in GROUPS[api].items())
            + ".\n"
        )
        order = [typ for c in GROUPS[api].values() for typ in c["types"]]
        types = sorted(types, key=lambda t: order.index(t["type"]))
    lines.append(collection_table(b, types, cwd, with_group=api in GROUPS))
    if api in VERSIONS:
        lines.append(VERSIONS[api])
    if api in PITFALLS:
        lines.append(PITFALLS[api])
    lines.append("## Voorbeelden (DuckDB)\n")
    if api == "bag":
        lines += [
            "Verwijzingen: `verblijfsobject.heeftAlsHoofdadres` → `nummeraanduiding`, "
            "`nummeraanduiding.ligtAan` → `openbareruimte`, `openbareruimte.ligtIn` → `woonplaats` "
            "(`nummeraanduiding.ligtIn` gaat voor indien aanwezig), `verblijfsobject.maaktDeelUitVan` "
            "(lijst) → `pand`. Koppel op `identificatie` en kies de versie van het doelobject die op "
            "dezelfde datum geldig was. `nummeraanduiding`, `openbareruimte` en `kenmerkinonderzoek` "
            "hebben geen geometrie.\n",
            b.recipe(
                "De verblijfsobjecten die vandaag geldig zijn in een pand (`maaktDeelUitVan` is een lijst):",
                f"""
                SELECT identificatie, gebruiksdoel, oppervlakte, status
                FROM '{p('verblijfsobject')}'
                WHERE list_contains(maaktDeelUitVan, '0307100000370278') AND {cur('bag')}
                """,
                cwd,
            ),
            b.recipe(
                "Verblijfsobjecten in gebruik per gebruiksdoel (een verblijfsobject met meer "
                "gebruiksdoelen telt in elke groep mee):",
                f"""
                SELECT g AS gebruiksdoel, count(*) AS aantal
                FROM '{p('verblijfsobject')}', unnest(gebruiksdoel) AS u(g)
                WHERE {cur('bag')} AND {IN_GEBRUIK}
                GROUP BY ALL ORDER BY aantal DESC
                """,
                cwd,
            ),
            b.recipe(
                "Hoeveel woningen er sinds 1 januari 2015 netto bij zijn gekomen, per wijk: de "
                "toestand nu min de toestand toen, met dezelfde definitie. Ter vergelijking het "
                "aantal woningen in panden met een bouwjaar vanaf 2015; dat mist de woningen die in "
                "oudere panden zijn gemaakt (kantoren omgebouwd, woningen gesplitst) en negeert wat "
                "verdwenen is:",
                f"""
                WITH w AS (
                  FROM '{p('verblijfsobject')}'
                  WHERE list_contains(gebruiksdoel, 'woonfunctie') AND {IN_GEBRUIK})
                SELECT wijkcode, any_value(wijknaam) AS wijknaam,
                       count(*) FILTER (WHERE beginGeldigheid <= DATE '2015-01-01'
                         AND (eindGeldigheid IS NULL OR eindGeldigheid > DATE '2015-01-01')) AS woningen_2015,
                       count(*) FILTER (WHERE {cur('bag')}) AS woningen_nu,
                       woningen_nu - woningen_2015 AS netto_erbij,
                       count(*) FILTER (WHERE {cur('bag')} AND bouwjaarPand >= 2015) AS in_nieuwbouw
                FROM w
                GROUP BY wijkcode ORDER BY netto_erbij DESC
                LIMIT 10
                """,
                cwd,
            ),
            b.recipe(
                "Als gesloopt geregistreerde panden van minstens 50 m² sinds 2020, naar wat er "
                "gebeurd is. De status van de versie ervoor ('Bouwvergunning verleend': nooit "
                "gebouwd) en de verblijfsobjecten van de dag voor de registratie: staan die nu in "
                "een ander pand, dan is het pand samengevoegd met een buurpand; zijn ze ingetrokken, "
                "dan is het echt gesloopt. Een pand zonder verblijfsobjecten is meestal een "
                "bijgebouw:",
                f"""
                WITH s AS (
                  SELECT identificatie, beginGeldigheid AS registratie, voorgaandeVersie
                  FROM '{p('pand')}'
                  WHERE {cur('bag')} AND status = 'Pand gesloopt'
                    AND beginGeldigheid >= DATE '2020-01-01' AND grondoppervlakte >= 50),
                ervoor AS (
                  SELECT s.identificatie, p.status
                  FROM s JOIN '{p('pand')}' p
                    ON p.identificatie = s.identificatie AND p.beginGeldigheid = s.voorgaandeVersie),
                vbo AS (
                  SELECT s.identificatie,
                         count(*) FILTER (WHERE nu.status = 'Verblijfsobject ingetrokken') AS ingetrokken,
                         count(*) FILTER (WHERE NOT list_contains(nu.maaktDeelUitVan, s.identificatie)
                           AND nu.status NOT IN ('Verblijfsobject ingetrokken',
                                                 'Niet gerealiseerd verblijfsobject')) AS elders
                  FROM s
                  JOIN '{p('verblijfsobject')}' toen
                    ON list_contains(toen.maaktDeelUitVan, s.identificatie)
                   AND toen.beginGeldigheid <= s.registratie - 1
                   AND (toen.eindGeldigheid IS NULL OR toen.eindGeldigheid > s.registratie - 1)
                  JOIN '{p('verblijfsobject')}' nu
                    ON nu.identificatie = toen.identificatie AND {cur('bag', 'nu')}
                  GROUP BY s.identificatie)
                SELECT CASE
                         WHEN ervoor.status = 'Bouwvergunning verleend' THEN 'nooit gebouwd'
                         WHEN vbo.elders > 0 THEN 'samengevoegd'
                         WHEN vbo.ingetrokken > 0 THEN 'gesloopt'
                         ELSE 'zonder verblijfsobjecten'
                       END AS soort,
                       count(*) AS panden
                FROM s LEFT JOIN ervoor USING (identificatie) LEFT JOIN vbo USING (identificatie)
                GROUP BY ALL ORDER BY panden DESC
                """,
                cwd,
            ),
            b.recipe(
                "Alle versies van een pand, de oudste eerst:",
                f"""
                SELECT voorkomenidentificatie, beginGeldigheid, eindGeldigheid, status, oorspronkelijkBouwjaar
                FROM '{p('pand')}'
                WHERE identificatie = '0307100000370278'
                ORDER BY voorkomenidentificatie
                """,
                cwd,
            ),
            b.recipe(
                "De gemeenten van een woonplaats (`gemeenteWoonplaatsRelatie` is JSON-tekst):",
                f"""
                SELECT naam, r ->> 'gemeentecode' AS gemeente, r ->> 'beginGeldigheid' AS sinds
                FROM '{p('woonplaats')}',
                     unnest(CAST(json(gemeenteWoonplaatsRelatie) AS JSON[])) AS u(r)
                WHERE {cur('bag')}
                """,
                cwd,
            ),
        ]
    elif api == "bgt":
        lines += [
            "De BGT-classificatie staat in `bgtFunctie`, `bgtFysiekVoorkomen` of `bgtType`, een "
            "fijnere IMGeo-classificatie in `plusFunctie`, `plusFysiekVoorkomen` of `plusType`; "
            "ontbreekt de plus-informatie, dan staat er een reden zoals `waardeOnbekend`. Alleen de "
            "objecten op maaiveld (`relatieveHoogteligging = 0`) samen bedekken het gebied zonder "
            "gaten en overlappingen; bruggen, overkappingen, tunnels en functionele gebieden zoals "
            "parken liggen erboven, eronder of overlappen ze. `bronhouder` is een code, bijvoorbeeld "
            "G0307 (gemeente Amersfoort); de namen staan in de codelijst "
            f"{API_BASE}/bgt/codelists/bronhouder. Een object hoort bij het gebied (`buurtcode` "
            "enzovoort) waarin een punt op zijn geometrie ligt, ook als het over de grens loopt.\n",
            b.recipe(
                "De verdeling van een buurt nu: de oppervlakte van de vlakken op maaiveld per "
                "objecttype, geknipt op de grens van de buurt, naast de som van de hele objecten met "
                "die buurtcode. De geknipte oppervlakten tellen op tot de oppervlakte van de buurt; "
                "bij water en wegen langs de grens wijkt de som op buurtcode sterk af:",
                f"""
                LOAD spatial;
                WITH grens AS (
                  SELECT geometrie AS g, geometrie_bbox AS bb
                  FROM '{rel(b, cwd, 'wijkenbuurten', 'buurt')}' WHERE code = 'BU03070100')
                SELECT parse_filename(filename, true) AS objecttype,
                       round(sum(ST_Area(ST_Intersection(v.geometrie, grens.g)))) AS m2_in_buurt,
                       round(sum(ST_Area(v.geometrie)) FILTER (WHERE v.buurtcode = 'BU03070100')) AS m2_op_buurtcode
                FROM read_parquet('topografie/*/*.parquet', union_by_name => true, filename => true) v, grens
                WHERE {cur('bgt', 'v')} AND v.relatieveHoogteligging = 0
                  AND v.geometrie_bbox.xmax >= grens.bb.xmin AND v.geometrie_bbox.xmin <= grens.bb.xmax
                  AND v.geometrie_bbox.ymax >= grens.bb.ymin AND v.geometrie_bbox.ymin <= grens.bb.ymax
                  AND ST_Intersects(v.geometrie, grens.g)
                GROUP BY ALL ORDER BY m2_in_buurt DESC
                """,
                cwd,
            ),
            b.recipe(
                "Wijzigingen in een periode: hoeveel wegdelen in de gemeente Amersfoort in 2025 "
                "nieuw, gewijzigd of beëindigd zijn (een object met meer versies telt één keer per "
                "soort):",
                f"""
                SELECT
                  count(DISTINCT identificatie) FILTER (WHERE tijdstipRegistratie >= TIMESTAMP '2025-01-01'
                    AND tijdstipRegistratie < TIMESTAMP '2026-01-01' AND voorgaandeVersie IS NULL) AS nieuw,
                  count(DISTINCT identificatie) FILTER (WHERE tijdstipRegistratie >= TIMESTAMP '2025-01-01'
                    AND tijdstipRegistratie < TIMESTAMP '2026-01-01' AND voorgaandeVersie IS NOT NULL) AS gewijzigd,
                  count(DISTINCT identificatie) FILTER (WHERE volgendeVersie IS NULL
                    AND eindRegistratie >= TIMESTAMP '2025-01-01' AND eindRegistratie < TIMESTAMP '2026-01-01') AS beeindigd
                FROM '{p('wegdeel')}'
                WHERE gemeentecode = '0307'
                """,
                cwd,
            ),
            b.recipe(
                "Bulkbewerkingen vinden: tijdstippen waarop één bronhouder honderden bestaande "
                "objecten tegelijk een nieuwe versie gaf (de eerste levering, zonder "
                "`voorgaandeVersie`, telt niet mee):",
                """
                SELECT bronhouder, tijdstipRegistratie, count(*) AS versies
                FROM read_parquet('*/*/*.parquet', union_by_name => true)
                WHERE voorgaandeVersie IS NOT NULL
                GROUP BY ALL HAVING count(*) >= 500
                ORDER BY versies DESC
                """,
                cwd,
            ),
            b.recipe(
                "Wie de bomen en hagen bijhoudt: vegetatieobjecten in de gemeente Amersfoort per "
                "soort en bronhouder (een laag aantal bij de gemeente betekent dat zij ze niet in de "
                "BGT bijhoudt, niet dat ze er niet zijn):",
                f"""
                SELECT plusType, bronhouder, count(*) AS aantal
                FROM '{p('vegetatieobject')}'
                WHERE {cur('bgt')} AND gemeentecode = '0307'
                GROUP BY ALL ORDER BY plusType, aantal DESC
                """,
                cwd,
            ),
            b.recipe(
                "De huisnummerlabels van een pand (`nummeraanduidingreeks` is JSON-tekst):",
                f"""
                SELECT identificatie, identificatieBAGPND, r ->> 'tekst' AS tekst,
                       r ->> 'identificatieBAGVBOLaagsteHuisnummer' AS vbo_laagste
                FROM '{p('pand')}',
                     unnest(CAST(json(nummeraanduidingreeks) AS JSON[])) AS u(r)
                WHERE {cur('bgt')} AND identificatieBAGPND = '0307100000370278'
                """,
                cwd,
            ),
        ]
    elif api == "wijkenbuurten":
        lines += [
            "Een gemeente is ingedeeld in wijken, een wijk in buurten. `code` is de CBS-code "
            "(gemeente 0307, wijk WK030701, buurt BU03070100); `wijk.gemeente`, `buurt.wijk` en "
            "`buurt.gemeente` zijn codes. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek. "
            "Geen historie: de stand van 1 januari 2026.\n",
            b.recipe(
                "De buurten van een wijk:",
                f"""
                SELECT b.code, b.naam, b.water
                FROM '{p('buurt')}' b JOIN '{p('wijk')}' w ON w.code = b.wijk
                WHERE w.naam = 'Stadskern' AND b.gemeente = '0307'
                ORDER BY b.code
                """,
                cwd,
            ),
        ]
    elif api == "postcode6":
        lines += [
            "Een rij per postcodegebied (bijvoorbeeld 3811LM) op 1 januari 2024, zonder historie. "
            "`gemeentecode`, `wijkcode` en `buurtcode` verwijzen naar de collecties in "
            "`../wijkenbuurten`; een postcodegebied hoort bij de buurt waarin een punt binnen het "
            "gebied ligt. Cijfers per buurt of wijk uit de Kerncijfers wijken en buurten van het CBS "
            "(WOZ-waarde, inkomen) zitten er niet in.\n",
            b.recipe(
                "Inwoners per buurt, opgeteld over de postcodegebieden (een ondergrens), met het "
                "aantal postcodes met en zonder waarde:",
                f"""
                SELECT buurtcode, sum(aantal_inwoners) AS inwoners_minstens,
                       count(aantal_inwoners) AS postcodes_met_waarde, count(*) AS postcodes
                FROM '{p('postcode6')}'
                GROUP BY ALL ORDER BY inwoners_minstens DESC NULLS LAST
                LIMIT 10
                """,
                cwd,
            ),
        ]
    return "\n".join(lines)


def group_md(b, api, group):
    cwd = b.catalog / api / group
    conf = GROUPS[api][group]
    types = [t for t in b.types if t["api"] == api and t["type"] in conf["types"]]
    return "\n".join(
        [
            f"# {conf['title']} ({api}/{group})\n",
            conf["description"] + "\n",
            "Versies, classificatie en voorbeelden: [AGENTS.md van de BGT](../AGENTS.md); algemene "
            "aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md).\n",
            collection_table(b, types, cwd),
        ]
    )


def collection_md(b, t):
    api, typ = t["api"], t["type"]
    cwd = b.parquet(t).parent
    f = f"{typ}.parquet"
    rows = b.db.sql(f"SELECT count(*) FROM '{b.parquet(t)}'").fetchone()[0]
    geoms = t["geometries"]
    to_root = os.path.relpath(b.catalog / "AGENTS.md", cwd)
    to_api = os.path.relpath(b.catalog / api / "AGENTS.md", cwd)
    lines = [f"# {t['label']} ({rel_dir(api, typ).as_posix()})\n"]
    lines.append(
        f"De collectie `{typ}` van de API {API_BASE}/{api} als één bestand, `{f}`, {n(rows)} rijen. "
        f"Algemene aanwijzingen: [AGENTS.md van de catalogus]({to_root}); versies en verwijzingen "
        f"van de registratie: [AGENTS.md van {api}]({to_api}). Beschrijvingen van de kolommen: "
        "`collection.json` (`table:columns`) en de README.\n"
    )
    if geoms:
        g = ", ".join(f"`{x['name']}`" + (" (primair)" if x["primary"] else "") for x in geoms)
        lines.append(f"- Geometriekolommen: {g}; CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.")
    else:
        lines.append("- Geen geometrie: een gewoon Parquet-bestand.")
    n_current = b.db.sql(f"SELECT count(*) FROM '{b.parquet(t)}' WHERE {cur(api)}").fetchone()[0]
    if api in CURRENT:
        lines.append(
            f"- Actuele versies: `WHERE {CURRENT[api]}`, {n(n_current)} rijen."
            + (
                " Geen: alle objecten in deze collectie zijn beëindigd, alleen de historie is er nog."
                if not n_current
                else ""
            )
        )
    lists = [c["name"] for c in t["columns"] if c["type"].startswith("array")]
    jsons = [c["name"] for c in t["columns"] if c["type"] == "json"]
    if lists:
        lines.append(f"- Lijsten: {', '.join('`' + x + '`' for x in lists)}.")
    if jsons:
        lines.append(f"- JSON-tekst (lijsten van objecten): {', '.join('`' + x + '`' for x in jsons)}.")
    refs = []
    first_ref = None
    for c in t["columns"]:
        if c["featureRef"]:
            target = b.ref_target(t, c)
            if target:
                refs.append(f"`{c['name']}` → `{rel_dir(*target).as_posix()}.{b.id_column[target]}`")
                first_ref = first_ref or (c, target)
    if refs:
        lines.append(f"- Verwijzingen: {', '.join(refs)}.")
    lines.append("")
    lines.append("## Voorbeelden (DuckDB)\n")
    where = cur(api) if n_current else "true"
    if api in CURRENT:
        title = "Vijf actuele versies:" if n_current else "Vijf versies:"
    else:
        title = "Vijf rijen:"
    exclude = f" EXCLUDE ({', '.join(x['name'] for x in geoms)})" if geoms else ""
    lines.append(b.recipe(title, f"SELECT *{exclude}\nFROM '{f}'\nWHERE {where}\nLIMIT 5", cwd))
    if first_ref:
        c, target = first_ref
        tid = b.id_column[target]
        on = (
            f"list_contains(t.{c['name']}, r.{tid})"
            if c["type"].startswith("array")
            else f"r.{tid} = t.{c['name']}"
        )
        tgeoms = geometry_names(b, *target)
        texclude = f" EXCLUDE ({', '.join(tgeoms)})" if tgeoms else ""
        sql = f"""
            SELECT t.{b.id_column[(api, typ)]}, r.*{texclude}
            FROM '{f}' t
            JOIN '{rel(b, cwd, *target)}' r ON {on} AND {cur(target[0], 'r')}
            WHERE {cur(api, 't') if n_current else 'true'}
            LIMIT 5
            """
        if b.has_rows(sql, cwd):
            lines.append(b.recipe(f"De verwijzing `{c['name']}` volgen:", sql, cwd))
    if api == "bgt":
        lines.append(bgt_values(b, typ))
    return "\n".join(lines)


def bgt_values(b, typ):
    """The value definitions of a BGT collection, from the skill (one source for both)."""
    path = b.repo / BGT_VALUES.format(typ=typ)
    if not path.exists():
        raise SystemExit(f"value definitions missing: {path}")
    text = path.read_text()
    # drop the title and the pointer to the skill's own reference file; headings one level down
    text = re.sub(r"\A# .*\n+", "", text)
    text = text.replace(" Hoe men de waarden opgeeft, staat in ../bgt.md.", "")
    if "../" in text:
        raise SystemExit(f"unresolved relative link in {path}")
    text = re.sub(r"^## ", "### ", text, flags=re.M)
    return "## Waarden en definities\n\n" + text.strip() + "\n"
