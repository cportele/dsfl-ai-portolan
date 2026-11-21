# Pand (bgt/topografie/pand)

De collectie `pand` van de API https://bag.ldproxy.net/bgt als één bestand, `pand.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.
- JSON-tekst (lijsten van objecten): `nummeraanduidingreeks`.
- Verwijzingen: `identificatieBAGPND` → `bag/pand.identificatie`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/pand/pand.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

De verwijzing `identificatieBAGPND` volgen:

```sql
SELECT t.identificatie, r.* EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/pand/pand.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet' r ON r.identificatie = t.identificatieBAGPND AND r.beginGeldigheid <= current_date AND (r.eindGeldigheid IS NULL OR r.eindGeldigheid > current_date)
WHERE t.eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Een PAND is de kleinste bij de totstandkoming functioneel en bouwkundig-constructief zelfstandige eenheid die direct en duurzaam met de aarde is verbonden en betreedbaar en afsluitbaar is. English: building footprint, as in the BAG (Basisregistratie Adressen en Gebouwen), with house number labels.

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.
