# Kast (bgt/inrichtingselementen/kast)

De collectie `kast` van de API https://bag.ldproxy.net/bgt als één bestand, `kast.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/kast/kast.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Object met een permanent karakter dat dient om iets in te bergen en te beschermen. English: cabinet: electricity, telecom, cable TV, traffic light control box (point).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeKastPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `CAI-kast`: Kast ten behoeve van de regeling van radio- en televisiesignalen.
- `elektrakast`: Kast ten behoeve van de regeling van het transport van elektriciteit.
- `gaskast`: Kast ten behoeve van de regeling van het transport van gas.
- `telecom kast`: Kast ten behoeve van de regeling van telecommunicatie.
- `rioolkast`: Kast ten behoeve van de regeling van het transport van rioolwater.
- `openbare verlichtingkast`: Kast ten behoeve van de regeling van de openbare verlichting.
- `verkeersregelinstallatiekast`: Kast ten behoeve van de regeling van het verkeer.
- `telkast`: Kast ten behoeve van het meten van permanente verkeertellingen.
- `GMS kast`: Kast ten behoeve van het meten van weers- en wegdekomstandigheden.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
