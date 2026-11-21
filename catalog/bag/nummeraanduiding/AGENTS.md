# Nummeraanduiding (bag/nummeraanduiding)

De collectie `nummeraanduiding` van de API https://bag.ldproxy.net/bag als één bestand, `nummeraanduiding.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bag](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geen geometrie: een gewoon Parquet-bestand.
- Actuele versies: `WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)`.
- Verwijzingen: `postcode` → `postcode6/postcode6.postcode`, `ligtAan` → `bag/openbareruimte.identificatie`, `ligtIn` → `bag/woonplaats.identificatie`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT *
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet'
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
LIMIT 5
```

De verwijzing `postcode` volgen:

```sql
SELECT t.identificatie, r.* EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet' r ON r.postcode = t.postcode
WHERE t.beginGeldigheid <= current_date AND (t.eindGeldigheid IS NULL OR t.eindGeldigheid > current_date)
LIMIT 5
```
