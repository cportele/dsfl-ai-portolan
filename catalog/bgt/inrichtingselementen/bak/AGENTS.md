# Bak (bgt/inrichtingselementen/bak)

De collectie `bak` van de API https://bag.ldproxy.net/bgt als één bestand, `bak.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/bak/bak.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Object met een permanent karakter dat dient om iets in te bergen of te verzamelen. English: container: waste bin, flower box, grit bin (point).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeBakPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `afval apart plaats`: Boven- of ondergrondse opslagplaats voor het gescheiden inzamelen van afval, met stortkoker(s) op het straatniveau.
- `afvalbak`: Bak of korf in de openbare ruimte met een permanent karakter; bedoeld voor het verzamelen van (meestal los) afval.
- `drinkbak`: Bak gevuld met water, waaruit vee of wild kan drinken.
- `bloembak`: Bak in de openbare ruimte met een permanent karakter, waarin planten of struiken zijn geplant.
- `zand- / zoutbak`: Een bak met strooisel ten behoeve van gladheidsbestrijding.
- `container`: Nagelvast met de grond verbonden inzamelmiddel voor afvalstoffen, doorgaans van metaal of kunststof waarin afvalstoffen worden verzameld, bewaard en waaruit deze afvalstoffen vervolgens worden overgeladen in een inzamelvoertuig.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
