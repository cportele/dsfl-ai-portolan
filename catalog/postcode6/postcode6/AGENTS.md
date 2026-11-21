# Postcodegebied (postcode6/postcode6)

De collectie `postcode6` van de API https://bag.ldproxy.net/postcode6 als één bestand, `postcode6.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van postcode6](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Verwijzingen: `gemeentecode` → `wijkenbuurten/gemeente.code`, `wijkcode` → `wijkenbuurten/wijk.code`, `buurtcode` → `wijkenbuurten/buurt.code`.

## Voorbeelden (DuckDB)

Vijf rijen:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet'
LIMIT 5
```

De verwijzing `gemeentecode` volgen:

```sql
SELECT t.postcode, r.* EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/gemeente/gemeente.parquet' r ON r.code = t.gemeentecode
LIMIT 5
```
