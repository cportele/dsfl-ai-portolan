---
name: dsfl-ai-amersfoort-geoparquet
description: Vragen over gebouwen, adressen, woningen, topografie, buurten en postcodegebieden in Amersfoort beantwoorden met de GeoParquet-bestanden van de Portolan-catalogus van DSFL AI (BAG en BGT met historie, CBS-wijken en -buurten 2026, CBS-postcodegebieden 2024), bevraagd met DuckDB-SQL.
---

# Amersfoort als GeoParquet (DSFL AI)

De catalogus bevat de BAG van de gemeente Amersfoort en de BGT van de omgeving van Amersfoort, beide met
de volledige historie, de gemeenten, wijken en buurten 2026 van het CBS en de postcodegebieden (PC6)
2024 van het CBS, als GeoParquet in een openbare S3-bucket, zonder inloggegevens. Gegevens buiten dit
gebied staan er niet in.

Catalogus (STAC, Portolan): https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/catalog.json

## Werkwijze

1. Lees eerst de AGENTS.md van de catalogus:
   https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/AGENTS.md.
   Die beschrijft de bestanden, hoe je ze leest, de valkuilen en wat een antwoord verandert.
2. Lees daarna de AGENTS.md van de subcatalogus en van de collecties die de vraag raakt (bijvoorbeeld
   `bag/AGENTS.md` en `bag/pand/AGENTS.md`); de kolommen staan in `collection.json` (`table:columns`).
3. Bevraag de bestanden met DuckDB-SQL (extensies `httpfs` en `spatial`), met de URL's uit de AGENTS.md.
   DuckDB leest via HTTPS alleen de rijgroepen en kolommen die nodig zijn; download de bestanden niet.
4. Tel, sommeer en groepeer in SQL, niet door rijen op te halen en zelf te tellen.
