# Kenmerk in onderzoek (bag/kenmerkinonderzoek)

De collectie `kenmerkinonderzoek` van de API https://bag.ldproxy.net/bag als één bestand, `kenmerkinonderzoek.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bag](../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geen geometrie: een gewoon Parquet-bestand.
- Actuele versies: `WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT *
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/kenmerkinonderzoek/kenmerkinonderzoek.parquet'
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
LIMIT 5
```
