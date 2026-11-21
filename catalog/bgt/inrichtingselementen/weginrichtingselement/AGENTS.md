# Weginrichtingselement (bgt/inrichtingselementen/weginrichtingselement)

De collectie `weginrichtingselement` van de API https://bag.ldproxy.net/bgt als één bestand, `weginrichtingselement.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/weginrichtingselement/weginrichtingselement.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Een ruimtelijk object dat dient voor de inrichting van de openbare weg. English: road furnishing: crash barrier, tree pit, cattle grid, speed bump (point, line or surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeWeginrichtingPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `molgoot`: Smalle goot (lijngeometrie) in de lengterichting van de verharding, met veelal een cirkelsegment als dwarsprofiel.
- `lijnafwatering`: Goot in de lengterichting van de verharding, niet zijnde molgoot. Bijvoorbeeld roostergoot en verholen goot.
- `wegmarkering`: Op of in het oppervlak van de verharding aangebrachte tekens ter geleiding, waarschuwing, regeling of informatie van het verkeer.
- `wildrooster`: Horizontaal raamwerk dat dient om wild de doorgang te beletten.
- `rooster`: Een rooster niet zijnde lijnafwatering of wildrooster.
- `geleideconstructie`: Bermbeveiligingsconstructie bedoeld voor fysieke geleiding van voertuigen die uit de koers zijn geraakt.
- `balustrade`: Een balustrade is een hekwerk of afzetting aan de rand van een overbrugging. Een balustrade beveiligt tegen het vallen.
- `boomspiegel`: Het stuk grond rondom de stam van een boom dat van boven toegankelijk is voor lucht en water.
- `verblindingswering`: Constructie bedoeld om verblinding van weggebruikers door tegenlicht te voorkomen.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
