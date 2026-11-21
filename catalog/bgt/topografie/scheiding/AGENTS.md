# Scheiding (bgt/topografie/scheiding)

De collectie `scheiding` van de API https://bag.ldproxy.net/bgt als één bestand, `scheiding.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/scheiding/scheiding.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Kunstmatig obstakel met een werende functie. English: separation: wall, fence, quay wall, noise barrier, sheet piling (line or surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtType (waardelijst TypeScheiding; BGT, authentiek)

- `muur`: Een scheiding gemaakt van steen.
- `kademuur`: Verticale wand ter scheiding van land en water, opgebouwd uit een muur van gemetselde stenen of gestort beton.
- `geluidsscherm`: Een scheiding bedoeld om geluidshinder in de buitenlucht te verminderen.
- `damwand`: Een grondkerende constructie die bestaat uit een verticaal in de grond geplaatste wand.
- `walbescherming`: Een nagenoeg verticale wand tot kering van grond om afkalving van water te voorkomen, niet zijnde een kademuur.
- `hek`: Een hekwerk of schutting, typisch ten behoeve van erfafscheiding.
- `niet-bgt`: Het object is geen BGT object.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusType (waardelijst TypeScheidingPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `draadraster`: Kunstmatige terreinafscheiding, niet zijnde een faunaraster, in de vorm van een overwegend houten, metalen of kunststoffen rechtopstaande palen met daartussen een of meerdere draden.
- `faunaraster`: Kunstmatig aangebrachte scheiding van metaaldraad tussen palen, bedoeld voor het leiden van dieren.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
