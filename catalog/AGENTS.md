# Amersfoort: BAG, BGT en CBS-gebieden (DSFL AI)

De gegevens achter de OGC API's op https://bag.ldproxy.net als GeoParquet: de BAG van de gemeente Amersfoort en
de BGT van de omgeving van Amersfoort, beide met de volledige historie, de gemeenten, wijken en
buurten 2026 van het CBS en de postcodegebieden (PC6) 2024 van het CBS. Een collectie per
objecttype van de API's, met de namen van de eigenschappen van de API als kolomnamen; de
beschrijvingen van de kolommen staan in elke `collection.json` (`table:columns`) en README.

| Subcatalogus | API | Collecties | Licentie |
|---|---|---|---|
| [`bag/`](bag/AGENTS.md) | https://bag.ldproxy.net/bag | 8 | CC0 1.0 |
| [`bgt/`](bgt/AGENTS.md) | https://bag.ldproxy.net/bgt | 30 | CC0 1.0 |
| [`wijkenbuurten/`](wijkenbuurten/AGENTS.md) | https://bag.ldproxy.net/wijkenbuurten | 3 | CC BY 4.0 (Bron: Centraal Bureau voor de Statistiek (CBS), Wijk- en Buurtkaart 2026) |
| [`postcode6/`](postcode6/AGENTS.md) | https://bag.ldproxy.net/postcode6 | 1 | CC BY 4.0 (© CBS, © ESRI Nederland; Bron: Centraal Bureau voor de Statistiek (CBS), CBS Postcode6 2024) |

Elke collectie is één bestand `<objecttype>.parquet` in een eigen map, met een eigen `AGENTS.md`.
De BGT is verdeeld in drie subcatalogi: `bgt/topografie`, `bgt/inrichtingselementen` en
`bgt/overig`. De AGENTS.md van de subcatalogi beschrijven de versies en de verwijzingen binnen een
registratie. De catalogus wordt gebouwd met de scripts in https://github.com/cportele/dsfl-ai-portolan; fouten en vragen:
https://github.com/cportele/dsfl-ai-portolan/issues.

## Dezelfde gegevens via de API's en MCP

De API's op https://bag.ldproxy.net leveren dezelfde gegevens, met opgeslagen zoekopdrachten en een proces om te
tellen en op te tellen; elke API is ook een MCP-server (`https://bag.ldproxy.net/<api>/mcp`). Voor agents die
de MCP-servers gebruiken is er een skill met de werkwijze en de valkuilen:
[dsfl-ai-gebouwde-omgeving](https://github.com/cportele/dsfl-ai/tree/master/skills/dsfl-ai-gebouwde-omgeving). De valkuilen hieronder en in de AGENTS.md van de
subcatalogi komen daaruit, voor wie de bestanden zelf bevraagt.

## De bestanden lezen

- De voorbeelden lezen de bestanden rechtstreeks uit de openbare S3-bucket `dsfl-ai-417829795942-eu-central-1-an`
  (eu-central-1), zonder inloggegevens; met een lokale kopie vervang je het begin van de URL door
  het pad van de kopie.
  - via HTTPS: `https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/<pad>`, bijvoorbeeld
    `https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet`; DuckDB (httpfs) leest dan met
    range-requests alleen de rijgroepen en kolommen die nodig zijn;
  - via S3: `s3://dsfl-ai-417829795942-eu-central-1-an/<pad>`. Wildcards in paden
    (`read_parquet('s3://dsfl-ai-417829795942-eu-central-1-an/bgt/topografie/*/*.parquet')`) werken alleen zo, niet via HTTPS;
    in DuckDB eerst `CREATE SECRET (TYPE s3, REGION 'eu-central-1');`.
- GeoParquet 2.0: geometrieën als WKB met het Parquet-type GEOMETRY, in het Rijksdriehoeksstelsel
  (EPSG:28992, Amersfoort / RD New, in meter, x = oost, y = noord). Met de spatial-extensie van
  DuckDB (`INSTALL spatial; LOAD spatial;`) heeft een geometriekolom het type GEOMETRY. Voor
  lengte- en breedtegraad eerst `SET geometry_always_xy = true;` (vanaf DuckDB 2.0 verplicht, anders
  weigert `ST_Transform`), dan `ST_Transform(geometrie, 'EPSG:28992', 'OGC:CRS84')`.
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
  optioneel en worden per bronhouder (gemeente, provincie, waterschap, Rijk) verschillend
  bijgehouden; een ontbrekende waarde van het CBS per postcode is 0 tot 4 of geheim, geen nul.

## Verwijzingen tussen de subcatalogi

- `gemeentecode`, `wijkcode` en `buurtcode` (BAG-panden, -verblijfsobjecten, -ligplaatsen en
  -standplaatsen, alle BGT-objecten, postcode6) = `code` van de collecties gemeente, wijk en buurt
  in `wijkenbuurten`. De codes zijn afgeleid uit de CBS Wijk- en Buurtkaart 2026, het zijn geen
  BAG- of BGT-gegevens. De buurtcode bevat ook de gemeentecode en de wijkcode: BU03070100 ligt in
  gemeente 0307, wijk WK030701.
- `nummeraanduiding.postcode` (BAG) = `postcode6.postcode`.
- `pand.identificatieBAGPND` (BGT) = `pand.identificatie` (BAG),
  `openbareruimtelabel.identificatieBAGOPR` (BGT) = `openbareruimte.identificatie` (BAG).

## Voorbeelden (DuckDB)

De adressen van de verblijfsobjecten die vandaag geldig zijn in postcode 3811LM, met het aantal inwoners van het postcodegebied:

```sql
SELECT o.naam AS straat, n.huisnummer, n.huisletter, n.huisnummertoevoeging, n.postcode,
       v.identificatie AS verblijfsobject, p.aantal_inwoners AS inwoners_pc6
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet' v
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet' n
  ON n.identificatie = v.heeftAlsHoofdadres AND n.beginGeldigheid <= current_date AND (n.eindGeldigheid IS NULL OR n.eindGeldigheid > current_date)
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/openbareruimte/openbareruimte.parquet' o
  ON o.identificatie = n.ligtAan AND o.beginGeldigheid <= current_date AND (o.eindGeldigheid IS NULL OR o.eindGeldigheid > current_date)
LEFT JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet' p ON p.postcode = n.postcode
WHERE v.beginGeldigheid <= current_date AND (v.eindGeldigheid IS NULL OR v.eindGeldigheid > current_date) AND n.postcode = '3811LM'
ORDER BY n.huisnummer, n.huisletter, n.huisnummertoevoeging
```

Woningen in gebruik per wijk, met de naam van de wijk (verblijfsobjecten met woonfunctie, ook met andere gebruiksdoelen, met de statussen voor 'in gebruik'):

```sql
SELECT w.code, w.naam, count(*) AS woningen
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet' v
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/wijk/wijk.parquet' w ON w.code = v.wijkcode
WHERE v.beginGeldigheid <= current_date AND (v.eindGeldigheid IS NULL OR v.eindGeldigheid > current_date) AND list_contains(v.gebruiksdoel, 'woonfunctie')
  AND v.status IN ('Verblijfsobject in gebruik', 'Verblijfsobject in gebruik (niet ingemeten)', 'Verbouwing verblijfsobject')
GROUP BY ALL ORDER BY woningen DESC
```

BGT-panden die nu in de registratie staan, met het oorspronkelijk bouwjaar uit de BAG:

```sql
SELECT g.identificatie AS bgt_pand, g.identificatieBAGPND, b.oorspronkelijkBouwjaar
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/pand/pand.parquet' g
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet' b
  ON b.identificatie = g.identificatieBAGPND AND b.beginGeldigheid <= current_date AND (b.eindGeldigheid IS NULL OR b.eindGeldigheid > current_date)
WHERE g.eindRegistratie IS NULL
LIMIT 10
```

Ruimtelijke selectie: de BAG-panden die vandaag geldig zijn in een vierkant van 200 m bij de Onze Lieve Vrouwetoren (155000, 463000, het centrale punt van het Rijksdriehoeksstelsel), met het zwaartepunt in lengte- en breedtegraad (eerst het filter op de bounding box, dan het exacte predicaat):

```sql
INSTALL spatial; LOAD spatial;
SET geometry_always_xy = true;
SELECT identificatie, oorspronkelijkBouwjaar,
       ST_AsText(ST_Transform(ST_Centroid(geometrie), 'EPSG:28992', 'OGC:CRS84')) AS zwaartepunt
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet'
WHERE geometrie_bbox.xmax >= 155000 AND geometrie_bbox.xmin <= 155200
  AND geometrie_bbox.ymax >= 463000 AND geometrie_bbox.ymin <= 463200
  AND ST_Intersects(geometrie, ST_MakeEnvelope(155000, 463000, 155200, 463200))
  AND beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
```
