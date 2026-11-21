# Spoor (bgt/overig/spoor)

De collectie `spoor` van de API https://bag.ldproxy.net/bgt als één bestand, `spoor.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/overig/spoor/spoor.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

De as van het spoor, dat wil zeggen het midden van twee stalen staven op een onderling vaste afstand, waarover trein, tram, of sneltram rijdt. English: railway track, tram track (centre line).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtFunctie (waardelijst FunctieSpoor; BGT, authentiek)

- `trein`: Spoor voor een railvoertuig voor de langere afstand dat sneller dan 45 km per uur kan, bestaande uit een enkele of een reeks van locomotieven, treinstellen en/of wagons.
- `sneltram`: Spoor voor een boven- danwel ondergrondse interlokale tram met een vrije baan.
- `tram`: Spoor voor een railvoertuig voor personenvervoer voor de korte afstand.
- `niet-bgt`: Het object is geen BGT object.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFunctie (waardelijst FunctieSpoorPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `(haven)kraan`: Spoorbaan waarop een hefkraan (bij een haven) zich voortbeweegt.
