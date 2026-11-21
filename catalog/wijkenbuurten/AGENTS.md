# Wijken en buurten 2026 (CBS)

De gegevens van de API https://bag.ldproxy.net/wijkenbuurten als GeoParquet, een collectie per objecttype; de kolomnamen zijn de namen van de eigenschappen van de API. Begin met de algemene aanwijzingen in de [AGENTS.md van de catalogus](../AGENTS.md).

| Collectie | Geometrie |
|---|---|
| [`gemeente`](gemeente/AGENTS.md) (Gemeente) | geometrie |
| [`wijk`](wijk/AGENTS.md) (Wijk) | geometrie |
| [`buurt`](buurt/AGENTS.md) (Buurt) | geometrie |

## Voorbeelden (DuckDB)

Een gemeente is ingedeeld in wijken, een wijk in buurten. `code` is de CBS-code (gemeente 0307, wijk WK030701, buurt BU03070100); `wijk.gemeente`, `buurt.wijk` en `buurt.gemeente` zijn codes. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek. Geen historie: de stand van 1 januari 2026.

De buurten van een wijk:

```sql
SELECT b.code, b.naam, b.water
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/buurt/buurt.parquet' b JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/wijkenbuurten/wijk/wijk.parquet' w ON w.code = b.wijk
WHERE w.naam = 'Stadskern' AND b.gemeente = '0307'
ORDER BY b.code
```
