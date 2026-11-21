# Put (bgt/inrichtingselementen/put)

De collectie `put` van de API https://bag.ldproxy.net/bgt als één bestand, `put.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/put/put.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Gegraven of geboorde kokervormige diepte waarin zich (vloei)stoffen bevinden. English: pit: manhole, drain, gully, fire hydrant, well (point).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypePutPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `benzine- / olieput`: Putdeksel die toegang geeft tot een benzine- of olietank ten behoeve van vullen, onderhoud of inspectie.
- `brandkraan / -put`: Op de drinkwaterleiding aangesloten kraan, of deksel van een put voor het plaatsen van een brandkraan, op of nabij de openbare weg, voor brandbestrijding.
- `drainageput`: Putdeksel welke toegang geeft naar een poreuze of geperforeerde buisleiding, aangebracht onder de grond om de afwatering van de grond te verbeteren.
- `gasput`: Deksel van een put met afsluitkraan ten behoeve van het ondergrondse leidingenstelsel voor gastransport.
- `inspectie- / rioolput`: Deksel van een constructie die toegang geeft tot een rioolstelsel.
- `kolk`: Deksel van een ingegraven bak voor de opvang en afvoer van neerslag afkomstig van erop aangesloten oppervlakken.
- `waterleidingput`: Deksel van een put met afsluitkraan ten behoeve van het ondergrondse leidingenstelsel voor watertransport.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
