# Pand (bag/pand)

De collectie `pand` van de API https://bag.ldproxy.net/bag als één bestand, `pand.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bag](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet'
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
LIMIT 5
```
