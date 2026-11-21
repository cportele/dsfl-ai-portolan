# Overbruggingsdeel (bgt/topografie/overbruggingsdeel)

De collectie `overbruggingsdeel` van de API https://bag.ldproxy.net/bgt als één bestand, `overbruggingsdeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/overbruggingsdeel/overbruggingsdeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Onderdeel van een beweegbare of vaste verbinding tussen twee punten, die door water, een weg of anderszins gescheiden zijn, dat essentieel is voor de constructie . English: bridge part: deck, abutment, pillar of a bridge or viaduct (surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### typeOverbruggingsdeel (waardelijst TypeOverbruggingsdeel; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `dek`: Direct door het verkeer belaste deel van de bovenbouw van de brug.
- `landhoofd`: Ondersteuningsconstructie ter plaatse van een overgang van de aardebaan naar een kunstwerk.
- `pijler`: Ondersteuningsconstructie van bruggen en soortgelijke kunstwerken.
- `sloof`: Deel van de pijler voor de overdracht van krachten naar de ondergrond of de fundering.
- `pyloon`: Boven de bovenbouw uitstekende draagconstructie voor tuien (kabels).

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.

### hoortBijTypeOverbrugging (waardelijst TypeOverbrugging; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `brug`: Kunstwerk over een watervlakte of waterloop, bestaande uit een losliggend, al of niet beweegbaar brugdek gesteund door pijlers en/of landhoofden.
- `aquaduct`: Kunstwerk waarmee een watergang door een bakvormige constructie over een weg, een spoorweg, een andere watergang, een leiding of een terrein wordt geleid.
- `viaduct`: Kunstwerk over een weg, spoorweg of terreinverdieping, bestaande uit een dek gesteund door pijlers en/of landhoofden.
- `fly-over`: Kunstwerk in de vorm van een viaduct dat deel uitmaakt van een verkeersbaan en waarmee een verkeersstroom over twee of meer ongelijkvloerse verkeersstromen wordt geleid.
- `ecoduct`: Wildwissel in de vorm van een viaduct voor passages van dieren over een weg of spoorweg.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
