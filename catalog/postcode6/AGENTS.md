# Postcodegebieden 2024 (CBS)

De gegevens van de API https://bag.ldproxy.net/postcode6 als GeoParquet, een collectie per objecttype; de kolomnamen zijn de namen van de eigenschappen van de API. Begin met de algemene aanwijzingen in de [AGENTS.md van de catalogus](../AGENTS.md).

| Collectie | Geometrie |
|---|---|
| [`postcode6`](postcode6/AGENTS.md) (Postcodegebied) | geometrie |

## Wat een antwoord verandert (postcode6)

- Aantallen zijn op vijftallen afgerond, percentages op tientallen. Het CBS publiceert een waarde
  alleen bij ten minste vijf inwoners, huishoudens of woningen (percentages bij ten minste tien):
  **een ontbrekende waarde is 0 tot 4 of geheim**, geen nul en geen onbekend aantal.
- **Sommen zijn ondergrenzen**, sommen van deelgroepen (leeftijdsklassen, huishoudtypen) nog meer;
  zeg "minstens" en hoeveel postcodes een waarde hebben (`count(kolom)` naast `count(*)`).
- **Percentages** en `gemiddelde_huishoudensgrootte` zijn niet op te tellen. Een gewogen gemiddelde
  telt alleen de postcodes met een waarde; `percentage_koopwoningen` en `percentage_huurwoningen`
  ontbreken zo vaak (vaak heeft een postcode er maar één van) dat er geen aandeel per wijk uit volgt.
- **Sorteren**: `ORDER BY ... DESC` zet in DuckDB de ontbrekende waarden achteraan, maar een
  vergelijking (`< 5`) treft een ontbrekende waarde nooit.

## Voorbeelden (DuckDB)

Een rij per postcodegebied (bijvoorbeeld 3811LM) op 1 januari 2024, zonder historie. Het uittreksel bevat 3.609 postcodegebieden in gemeente 0307 en 4 daarbuiten (3851DP in gemeente 0233; 2324VE in gemeente 0546; 3818MZ in gemeente 0327; 3181EM in gemeente 0599), die adressen in de BAG van dit uittreksel hebben. <!-- claim-check: de postcodegebieden buiten de gemeente hebben adressen in de BAG van dit uittreksel
SELECT p.postcode FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet' p
WHERE p.gemeentecode <> '0307'
  AND p.postcode NOT IN (SELECT postcode FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet' WHERE postcode IS NOT NULL)
-->
`gemeentecode`, `wijkcode` en `buurtcode` verwijzen naar de collecties in `../wijkenbuurten`; een postcodegebied hoort bij de buurt waarin een punt binnen het gebied ligt. Cijfers per buurt of wijk uit de Kerncijfers wijken en buurten van het CBS (WOZ-waarde, inkomen) zitten er niet in.

Inwoners per buurt, opgeteld over de postcodegebieden (een ondergrens), met het aantal postcodes met en zonder waarde:

```sql
SELECT buurtcode, sum(aantal_inwoners) AS inwoners_minstens,
       count(aantal_inwoners) AS postcodes_met_waarde, count(*) AS postcodes
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet'
GROUP BY ALL ORDER BY inwoners_minstens DESC NULLS LAST
LIMIT 10
```
