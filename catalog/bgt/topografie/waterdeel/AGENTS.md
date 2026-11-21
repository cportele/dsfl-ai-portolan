# Waterdeel (bgt/topografie/waterdeel)

De collectie `waterdeel` van de API https://bag.ldproxy.net/bgt als één bestand, `waterdeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/waterdeel/waterdeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Kleinste functioneel onafhankelijk stukje water met gelijkblijvende, homogene eigenschappen en relaties dat er binnen het objecttype Water van NEN 3610 wordt onderscheiden en dat permanent met water bedekt is. English: water body: watercourse, canal, ditch, lake, pond (surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtType (waardelijst TypeWater; BGT, authentiek)

- `zee`: Uitgestrekt oppervlak zout water.
- `waterloop`: Een voor de waterbeheersing bestemde geul die meestal permanent water bevat (zoals rivier, kanaal, beek, sloot, gracht).
- `watervlakte`: Alle oppervlakken die vrij permanent met zoet water zijn bedekt. (zoals meer, plas, ven, vijver).
- `greppel, droge sloot`: Een ten behoeve van de waterbeheersing gegraven geul die al dan niet met water bedekt is.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusType (waardelijst TypeWaterPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `rivier`: Het water, dat ten atmosferische neerslag op hellende terreinen valt, vloeit, voor zover het niet verdampt of door planten wordt opgenomen, tezamen tot een waterloop en stroomt naar laaggelegen streken. Zulk een natuurlijke afvloeiing heet een rivier.
- `sloot`: Algemene benaming voor een waterloop van beperkte breedte die stilstaand of slechts langzaam stromend water bevat.
- `kanaal`: Een gegraven grote waterloop die dient voor scheepvaart en/of watertransport.
- `beek`: Een natuurlijke smalle waterloop zonder getij.
- `gracht`: Een gracht is een gegraven greppel met water, die hoofdzakelijk voorkomt in oude steden.
- `bron`: Grondwater dat op natuurlijke wijze uit het aardoppervlak tevoorschijn komt.
- `haven`: Een tot ligplaats van schepen geschikt, natuurlijk of gegraven waterbekken aan zee of aan de oever van een rivier of binnenwater, dat beschutting biedt tegen wind en golven.
- `meer, plas, ven, vijver`: Een massa stilstaand landoppervlaktewater.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
