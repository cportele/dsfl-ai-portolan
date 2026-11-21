# Ligplaats (bag/ligplaats)

De collectie `ligplaats` van de API https://bag.ldproxy.net/bag als één bestand, `ligplaats.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bag](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)`.
- Lijsten: `heeftAlsNevenadres`.
- Verwijzingen: `heeftAlsHoofdadres` → `bag/nummeraanduiding.identificatie`, `heeftAlsNevenadres` → `bag/nummeraanduiding.identificatie`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/ligplaats/ligplaats.parquet'
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
LIMIT 5
```

De verwijzing `heeftAlsHoofdadres` volgen:

```sql
SELECT t.identificatie, r.*
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/ligplaats/ligplaats.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet' r ON r.identificatie = t.heeftAlsHoofdadres AND r.beginGeldigheid <= current_date AND (r.eindGeldigheid IS NULL OR r.eindGeldigheid > current_date)
WHERE t.beginGeldigheid <= current_date AND (t.eindGeldigheid IS NULL OR t.eindGeldigheid > current_date)
LIMIT 5
```
