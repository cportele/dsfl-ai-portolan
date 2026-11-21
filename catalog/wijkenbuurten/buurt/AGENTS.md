# Buurt (wijkenbuurten/buurt)

De collectie `buurt` van de API https://bag.ldproxy.net/wijkenbuurten als één bestand, `buurt.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van wijkenbuurten](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Verwijzingen: `wijk` → `wijkenbuurten/wijk.code`, `gemeente` → `wijkenbuurten/gemeente.code`.

## Voorbeelden (DuckDB)

Vijf rijen:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/buurt/buurt.parquet'
LIMIT 5
```

De verwijzing `wijk` volgen:

```sql
SELECT t.code, r.* EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/buurt/buurt.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/wijk/wijk.parquet' r ON r.code = t.wijk
LIMIT 5
```
