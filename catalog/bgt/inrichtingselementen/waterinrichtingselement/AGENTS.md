# Waterinrichtingselement (bgt/inrichtingselementen/waterinrichtingselement)

De collectie `waterinrichtingselement` van de API https://bag.ldproxy.net/bgt als één bestand, `waterinrichtingselement.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/waterinrichtingselement/waterinrichtingselement.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Een ruimtelijk object ter inrichting van het water. English: water furnishing: mooring post, buoy, fish ladder (point or line).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeWaterinrichtingPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `remmingswerk`: Constructie langs de opstelruimte en wachtruimte bedoeld voor het afmeren van schepen.
- `betonning`: Een systeem van boeien en bakens, waarmee in open zee of in een vaarwater ondiepten of de aanwezigheid van gevaarlijke objecten worden aangegeven.
- `geleidewerk`: Fuikvormige constructie aansluitend aan het hoofd van een kunstwerk voor het geven van mechanische en visuele geleiding tijdens het invaren van dat kunstwerk.
- `vuilvang`: Een voorziening om de waterloop dan wel één of meerdere objecten benedenstrooms te vrijwaren van drijvend vuil en dergelijke.
- `meerpaal`: Paal voor een kade of in een haven waaraan een schip kan worden afgemeerd.
- `hoogtemerk`: Relatief permanent merk, natuurlijk of kunstmatig, met daarin een punt met een bekende hoogte ten opzichte van een bepaald referentievlak.
