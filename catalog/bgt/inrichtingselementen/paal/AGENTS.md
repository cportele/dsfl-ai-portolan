# Paal (bgt/inrichtingselementen/paal)

De collectie `paal` van de API https://bag.ldproxy.net/bgt als één bestand, `paal.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/paal/paal.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Langwerpig stuk hout, ijzer, steen enz., dat in de grond staat. English: pole: lamp post, bollard, hectometre post, traffic light (point).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypePaalPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `lichtmast`: Mast bestemd voor het dragen van een of meer verlichtingsarmaturen.
- `telpaal`: Paal waaraan de verkeersteller is bevestigd.
- `portaal`: Geheel van twee of meer ondersteuningsconstructies die door een ligger zijn verbonden, bedoelt voor het aanbrengen van verkeersaanduidingen.
- `verkeersregelinstallatiepaal`: Paal met daaraan bevestigd de verkeersregelinstallatie.
- `verkeersbordpaal`: Paal waaraan een of meerdere verkeersborden zijn bevestigd.
- `poller`: Een poller of inzinkbare paal is een paal die door een elektrische of hydraulische aandrijving uit een wegdek omhoog wordt gestuurd en die dient om het autoverkeer te reguleren.
- `haltepaal`: Paal met daarop de dienstregeling ten behoeve van het openbaar vervoer.
- `vlaggenmast`: Paal bedoeld om vlaggen aan te hangen.
- `afsluitpaal`: Al dan niet verwijderbare paal in de grond om de weg of een gedeelte hiervan af te sluiten.
- `praatpaal`: Stalen of kunststof paal langs verkeerswegen welke bedoeld is telefonisch contact te leggen met een centrale meldkamer (ANWB).
- `hectometerpaal`: Paaltje of bordje geplaatst langs de weg, waarop een hectometerwaarde (weg) of kilometrering (vaarweg) is vermeld eventueel gevolgd door een letter.
- `dijkpaal`: Een markant punt op de waterkering of op het strand dat dient als referentiepunt voor afstandsaanduidingen.
- `drukknoppaal`: Paal met een lengte van ongeveer 1 m, met drukknop waarmee de verkeersdeelnemer zich meldt bij een verkeersregelinstallatie.
- `grensmarkering`: Paal ter afbakening van een grens.
- `sirene`: Een apparaat dat geluiden van variabele toonhoogte kan voortbrengen met als functie waarschuwingsdoeleinden.
