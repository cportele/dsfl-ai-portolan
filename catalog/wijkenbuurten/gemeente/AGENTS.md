# Gemeente (wijkenbuurten/gemeente)

De collectie `gemeente` van de API https://bag.ldproxy.net/wijkenbuurten als één bestand, `gemeente.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van wijkenbuurten](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.

## Voorbeelden (DuckDB)

Vijf rijen:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/gemeente/gemeente.parquet'
LIMIT 5
```
