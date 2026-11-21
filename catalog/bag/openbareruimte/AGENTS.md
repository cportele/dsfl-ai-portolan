# Openbare ruimte (bag/openbareruimte)

De collectie `openbareruimte` van de API https://bag.ldproxy.net/bag als één bestand, `openbareruimte.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bag](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geen geometrie: een gewoon Parquet-bestand.
- Actuele versies: `WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)`.
- Verwijzingen: `ligtIn` → `bag/woonplaats.identificatie`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT *
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/openbareruimte/openbareruimte.parquet'
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
LIMIT 5
```

De verwijzing `ligtIn` volgen:

```sql
SELECT t.identificatie, r.* EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/openbareruimte/openbareruimte.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/woonplaats/woonplaats.parquet' r ON r.identificatie = t.ligtIn AND r.beginGeldigheid <= current_date AND (r.eindGeldigheid IS NULL OR r.eindGeldigheid > current_date)
WHERE t.beginGeldigheid <= current_date AND (t.eindGeldigheid IS NULL OR t.eindGeldigheid > current_date)
LIMIT 5
```
