# OverigBouwwerk (bgt/topografie/overigbouwwerk)

De collectie `overigbouwwerk` van de API https://bag.ldproxy.net/bgt als één bestand, `overigbouwwerk.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/overigbouwwerk/overigbouwwerk.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Met de aarde verbonden duurzaam bouwwerk, dat niet valt onder de definities van een pand of kunstwerk. English: other structure: shed, canopy, storage tank, wind turbine, basin (surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtType (waardelijst TypeOverigBouwwerk; BGT, authentiek)

- `overkapping`: Een afzonderlijk staande overdekking rustend op kolommen.
- `open loods`: Niet verplaatsbaar licht gebouw met een open gevel, bestemd als berg- of werkplaats of als tijdelijk onderdak voor andere doeleinden.
- `opslagtank`: Opslagfaciliteit voor vloeistoffen, gassen of energie.
- `bezinkbak`: Een gesloten reservoir waarin het afvalwater tijdelijk wordt opgevangen met een slibreinigende voorziening.
- `windturbine`: Turbine waarin winddruk omgezet wordt in mechanische energie.
- `lage trafo`: Bouwwerk waarin transformator(en) zijn geplaatst voor elektriciteitsvoorziening.
- `bassin`: Waterbak, zoals een zwembad of een dok.
- `niet-bgt`: Het object is geen BGT object.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusType (waardelijst TypeOverigBouwwerkPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `bunker`: Een bunker is een van oorsprong militair verdedigingswerk dat een zekere mate van bescherming bood tegen beschietingen en bombardementen.
- `schuur`: Een vrijstaand, al of niet prefab, niet-vergunningsplichtig bouwwerk dat gebruikt wordt om goederen in op te slaan en ook als werkruimte kan dienen.
- `voedersilo`: Opslagfaciliteit voor veevoer, bestaande uit een verticale container met een opening aan de onderkant.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
