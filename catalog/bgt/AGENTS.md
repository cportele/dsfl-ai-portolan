# Basisregistratie Grootschalige Topografie (BGT)

De gegevens van de API https://bag.ldproxy.net/bgt als GeoParquet, een collectie per objecttype; de kolomnamen zijn de namen van de eigenschappen van de API. Begin met de algemene aanwijzingen in de [AGENTS.md van de catalogus](../AGENTS.md).

De collecties zijn verdeeld in subcatalogi: [Topografie (vlakken)](topografie/AGENTS.md) (`topografie`), [Inrichtingselementen](inrichtingselementen/AGENTS.md) (`inrichtingselementen`), [Overige objecten](overig/AGENTS.md) (`overig`).

| Collectie | Subcatalogus | Geometrie |
|---|---|---|
| [`wegdeel`](topografie/wegdeel/AGENTS.md) (Wegdeel) | `topografie` | geometrie, kruinlijn |
| [`ondersteunendwegdeel`](topografie/ondersteunendwegdeel/AGENTS.md) (OndersteunendWegdeel) | `topografie` | geometrie, kruinlijn |
| [`begroeidterreindeel`](topografie/begroeidterreindeel/AGENTS.md) (BegroeidTerreindeel) | `topografie` | geometrie, kruinlijn |
| [`onbegroeidterreindeel`](topografie/onbegroeidterreindeel/AGENTS.md) (OnbegroeidTerreindeel) | `topografie` | geometrie, kruinlijn |
| [`waterdeel`](topografie/waterdeel/AGENTS.md) (Waterdeel) | `topografie` | geometrie |
| [`ondersteunendwaterdeel`](topografie/ondersteunendwaterdeel/AGENTS.md) (OndersteunendWaterdeel) | `topografie` | geometrie |
| [`pand`](topografie/pand/AGENTS.md) (Pand) | `topografie` | geometrie |
| [`overigbouwwerk`](topografie/overigbouwwerk/AGENTS.md) (OverigBouwwerk) | `topografie` | geometrie |
| [`kunstwerkdeel`](topografie/kunstwerkdeel/AGENTS.md) (Kunstwerkdeel) | `topografie` | geometrie |
| [`overbruggingsdeel`](topografie/overbruggingsdeel/AGENTS.md) (Overbruggingsdeel) | `topografie` | geometrie |
| [`scheiding`](topografie/scheiding/AGENTS.md) (Scheiding) | `topografie` | geometrie |
| [`bak`](inrichtingselementen/bak/AGENTS.md) (Bak) | `inrichtingselementen` | geometrie |
| [`bord`](inrichtingselementen/bord/AGENTS.md) (Bord) | `inrichtingselementen` | geometrie |
| [`installatie`](inrichtingselementen/installatie/AGENTS.md) (Installatie) | `inrichtingselementen` | geometrie |
| [`kast`](inrichtingselementen/kast/AGENTS.md) (Kast) | `inrichtingselementen` | geometrie |
| [`mast`](inrichtingselementen/mast/AGENTS.md) (Mast) | `inrichtingselementen` | geometrie |
| [`paal`](inrichtingselementen/paal/AGENTS.md) (Paal) | `inrichtingselementen` | geometrie |
| [`put`](inrichtingselementen/put/AGENTS.md) (Put) | `inrichtingselementen` | geometrie |
| [`sensor`](inrichtingselementen/sensor/AGENTS.md) (Sensor) | `inrichtingselementen` | geometrie |
| [`straatmeubilair`](inrichtingselementen/straatmeubilair/AGENTS.md) (Straatmeubilair) | `inrichtingselementen` | geometrie |
| [`waterinrichtingselement`](inrichtingselementen/waterinrichtingselement/AGENTS.md) (Waterinrichtingselement) | `inrichtingselementen` | geometrie |
| [`weginrichtingselement`](inrichtingselementen/weginrichtingselement/AGENTS.md) (Weginrichtingselement) | `inrichtingselementen` | geometrie |
| [`vegetatieobject`](inrichtingselementen/vegetatieobject/AGENTS.md) (VegetatieObject) | `inrichtingselementen` | geometrie |
| [`spoor`](overig/spoor/AGENTS.md) (Spoor) | `overig` | geometrie |
| [`functioneelgebied`](overig/functioneelgebied/AGENTS.md) (FunctioneelGebied) | `overig` | geometrie |
| [`gebouwinstallatie`](overig/gebouwinstallatie/AGENTS.md) (GebouwInstallatie) | `overig` | geometrie |
| [`tunneldeel`](overig/tunneldeel/AGENTS.md) (Tunneldeel) | `overig` | geometrie |
| [`overigescheiding`](overig/overigescheiding/AGENTS.md) (OverigeScheiding) | `overig` | geometrie |
| [`ongeclassificeerdobject`](overig/ongeclassificeerdobject/AGENTS.md) (OngeclassificeerdObject) | `overig` | geometrie |
| [`openbareruimtelabel`](overig/openbareruimtelabel/AGENTS.md) (OpenbareRuimteLabel) | `overig` | geometrie |

## Versies (BGT)

Elke rij is een versie van een object, met als sleutel `identificatie` + `tijdstipRegistratie`. De
versies van een object sluiten naadloos op elkaar aan, van `tijdstipRegistratie` (inclusief) tot
`eindRegistratie` (exclusief). De versies die nu in de registratie staan, zoals de API die zonder
`datetime` levert (alleen bestaande objecten), hier geteld per bronhouder:

```sql
SELECT bronhouder, count(*) AS wegdelen
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/wegdeel/wegdeel.parquet'
WHERE eindRegistratie IS NULL
GROUP BY ALL ORDER BY wegdelen DESC
```

Op een tijdstip `T`: `tijdstipRegistratie <= T AND (eindRegistratie IS NULL OR eindRegistratie > T)`.
Een beëindigd object houdt zijn laatste versie, met `eindRegistratie` op de dag van
`objectEindTijd` (een datum; `eindRegistratie` is een tijdstip, vergelijk dus `eindRegistratie::date`).

<!-- claim-check: identificatie + tijdstipRegistratie is uniek, hoogstens één versie zonder eindRegistratie, eindRegistratie van de laatste versie op de dag van objectEindTijd
CREATE SECRET IF NOT EXISTS (TYPE s3, REGION 'eu-central-1');
WITH v AS (FROM read_parquet('s3://dsfl-ai-417829795942-eu-central-1-an/bgt/*/*/*.parquet', union_by_name => true))
SELECT identificatie FROM v GROUP BY identificatie, tijdstipRegistratie HAVING count(*) > 1
UNION ALL
SELECT identificatie FROM v WHERE eindRegistratie IS NULL GROUP BY identificatie HAVING count(*) > 1
UNION ALL
SELECT identificatie FROM v
WHERE volgendeVersie IS NULL AND objectEindTijd IS NOT NULL
  AND eindRegistratie::date IS DISTINCT FROM objectEindTijd
-->

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
  liggen erboven, eronder of overlappen ze.
- **Oppervlakte in een gebied**: een object hoort bij de buurt (`buurtcode`) waarin een punt op zijn
  geometrie ligt, ook als het over de grens loopt. Voor water en grote wegen kan dat tientallen
  procenten schelen; knip daarom met de grens uit `wijkenbuurten` (voorbeeld hieronder). Het totaal
  voor een aandeel is de som van de geknipte vlakken op maaiveld.
- **Groen en erf**: `begroeidterreindeel` is het groen; `onbegroeidterreindeel` met
  `bgtFysiekVoorkomen = 'erf'` is de grond bij een pand (tuinen, binnenplaatsen, opritten). Een
  aandeel groen bevat dus geen tuinen; noem het aandeel erf erbij.
- **IMGeo-plus en inrichtingselementen** (bomen, hagen, lichtmasten, putten, banken) zijn
  optioneel en alleen gevuld waar de bronhouder ze bijhoudt. Groepeer eerst op `bronhouder` (G...
  gemeente, P... provincie, W... waterschap, L... Rijk) en zeg "in de BGT geregistreerd" en door wie.
  `plusFysiekVoorkomen = 'waardeOnbekend'` kan een groot deel van de wegoppervlakte zijn;
  `bgtFysiekVoorkomen` is volledig.
- **Waarden**: een waarde met een dubbele punt verfijnt de waarde ervoor (`'recreatie: speeltuin'`
  is een soort `'recreatie'`; alle soorten met `LIKE 'recreatie%'`). `transitie` komt voor bij
  bgtFunctie en bgtType, maar staat in geen waardelijst. De definities van de waarden staan in de
  AGENTS.md van elke collectie.

## Voorbeelden (DuckDB)

De BGT-classificatie staat in `bgtFunctie`, `bgtFysiekVoorkomen` of `bgtType`, een fijnere IMGeo-classificatie in `plusFunctie`, `plusFysiekVoorkomen` of `plusType`; ontbreekt de plus-informatie, dan staat er een reden zoals `waardeOnbekend`. Alleen de objecten op maaiveld (`relatieveHoogteligging = 0`) samen bedekken het gebied zonder gaten en overlappingen; bruggen, overkappingen, tunnels en functionele gebieden zoals parken liggen erboven, eronder of overlappen ze. `bronhouder` is een code, bijvoorbeeld G0307 (gemeente Amersfoort); de namen staan in de codelijst https://bag.ldproxy.net/bgt/codelists/bronhouder. Een object hoort bij het gebied (`buurtcode` enzovoort) waarin een punt op zijn geometrie ligt, ook als het over de grens loopt.

De verdeling van een buurt nu: de oppervlakte van de vlakken op maaiveld per objecttype, geknipt op de grens van de buurt, naast de som van de hele objecten met die buurtcode. De geknipte oppervlakten tellen op tot de oppervlakte van de buurt; bij water en wegen langs de grens wijkt de som op buurtcode sterk af:

```sql
INSTALL spatial; LOAD spatial;
CREATE SECRET IF NOT EXISTS (TYPE s3, REGION 'eu-central-1');
WITH grens AS (
  SELECT geometrie AS g, geometrie_bbox AS bb
  FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/buurt/buurt.parquet' WHERE code = 'BU03070100')
SELECT parse_filename(filename, true) AS objecttype,
       round(sum(ST_Area(ST_Intersection(v.geometrie, grens.g)))) AS m2_in_buurt,
       round(sum(ST_Area(v.geometrie)) FILTER (WHERE v.buurtcode = 'BU03070100')) AS m2_op_buurtcode
FROM read_parquet('s3://dsfl-ai-417829795942-eu-central-1-an/bgt/topografie/*/*.parquet', union_by_name => true, filename => true) v, grens
WHERE v.eindRegistratie IS NULL AND v.relatieveHoogteligging = 0
  AND v.geometrie_bbox.xmax >= grens.bb.xmin AND v.geometrie_bbox.xmin <= grens.bb.xmax
  AND v.geometrie_bbox.ymax >= grens.bb.ymin AND v.geometrie_bbox.ymin <= grens.bb.ymax
  AND ST_Intersects(v.geometrie, grens.g)
GROUP BY ALL ORDER BY m2_in_buurt DESC
```

<!-- claim-check: De geknipte oppervlakten op maaiveld tellen op tot de oppervlakte van de buurt (minder dan 1 m² verschil):
INSTALL spatial; LOAD spatial;
CREATE SECRET IF NOT EXISTS (TYPE s3, REGION 'eu-central-1');
WITH grens AS (
  SELECT geometrie AS g, geometrie_bbox AS bb
  FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/buurt/buurt.parquet' WHERE code = 'BU03070100'),
som AS (
  SELECT sum(ST_Area(ST_Intersection(v.geometrie, grens.g))) AS m2
  FROM read_parquet('s3://dsfl-ai-417829795942-eu-central-1-an/bgt/topografie/*/*.parquet', union_by_name => true) v, grens
  WHERE v.eindRegistratie IS NULL AND v.relatieveHoogteligging = 0
    AND v.geometrie_bbox.xmax >= grens.bb.xmin AND v.geometrie_bbox.xmin <= grens.bb.xmax
    AND v.geometrie_bbox.ymax >= grens.bb.ymin AND v.geometrie_bbox.ymin <= grens.bb.ymax
    AND ST_Intersects(v.geometrie, grens.g))
SELECT som.m2, ST_Area(grens.g) AS buurt FROM som, grens WHERE abs(som.m2 - ST_Area(grens.g)) >= 1
-->

Wijzigingen in een periode: hoeveel wegdelen in de gemeente Amersfoort in 2025 nieuw, gewijzigd of beëindigd zijn (een object met meer versies telt één keer per soort):

```sql
SELECT
  count(DISTINCT identificatie) FILTER (WHERE tijdstipRegistratie >= TIMESTAMP '2025-01-01'
    AND tijdstipRegistratie < TIMESTAMP '2026-01-01' AND voorgaandeVersie IS NULL) AS nieuw,
  count(DISTINCT identificatie) FILTER (WHERE tijdstipRegistratie >= TIMESTAMP '2025-01-01'
    AND tijdstipRegistratie < TIMESTAMP '2026-01-01' AND voorgaandeVersie IS NOT NULL) AS gewijzigd,
  count(DISTINCT identificatie) FILTER (WHERE volgendeVersie IS NULL
    AND eindRegistratie >= TIMESTAMP '2025-01-01' AND eindRegistratie < TIMESTAMP '2026-01-01') AS beeindigd
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/wegdeel/wegdeel.parquet'
WHERE gemeentecode = '0307'
```

Bulkbewerkingen vinden: tijdstippen waarop één bronhouder honderden bestaande objecten tegelijk een nieuwe versie gaf (de eerste levering, zonder `voorgaandeVersie`, telt niet mee):

```sql
CREATE SECRET IF NOT EXISTS (TYPE s3, REGION 'eu-central-1');
SELECT bronhouder, tijdstipRegistratie, count(*) AS versies
FROM read_parquet('s3://dsfl-ai-417829795942-eu-central-1-an/bgt/*/*/*.parquet', union_by_name => true)
WHERE voorgaandeVersie IS NOT NULL
GROUP BY ALL HAVING count(*) >= 500
ORDER BY versies DESC
```

Wie de bomen en hagen bijhoudt: vegetatieobjecten in de gemeente Amersfoort per soort en bronhouder (een laag aantal bij de gemeente betekent dat zij ze niet in de BGT bijhoudt, niet dat ze er niet zijn):

```sql
SELECT plusType, bronhouder, count(*) AS aantal
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/vegetatieobject/vegetatieobject.parquet'
WHERE eindRegistratie IS NULL AND gemeentecode = '0307'
GROUP BY ALL ORDER BY plusType, aantal DESC
```

De huisnummerlabels van een pand (`nummeraanduidingreeks` is JSON-tekst):

```sql
SELECT identificatie, identificatieBAGPND, r ->> 'tekst' AS tekst,
       r ->> 'identificatieBAGVBOLaagsteHuisnummer' AS vbo_laagste
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/pand/pand.parquet',
     unnest(CAST(json(nummeraanduidingreeks) AS JSON[])) AS u(r)
WHERE eindRegistratie IS NULL AND identificatieBAGPND = '0307100000370278'
```
