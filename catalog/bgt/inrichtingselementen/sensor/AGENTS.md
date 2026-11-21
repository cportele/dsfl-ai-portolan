# Sensor (bgt/inrichtingselementen/sensor)

De collectie `sensor` van de API https://bag.ldproxy.net/bgt als één bestand, `sensor.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/sensor/sensor.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Apparaat voor de meting van een fysieke grootheid (bijv. temperatuur, licht, druk, elektriciteit). English: sensor: induction loop, camera, weather station (point or line).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeSensorPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `camera`: Installatie voor de registratie van beelden van situaties, waarvan directe observatie moeilijk of niet permanent mogelijk is.
- `debietmeter`: Een instrument dat de (afvoer)capaciteit van de volumestroom meet.
- `hoogtedetectieapparaat`: Een mechanisch of elektronisch waarschuwingssysteem, dat in werking treedt bij overschrijding van de aangegeven maximale doorrijhoogte.
- `detectielus`: In de verharding opgenomen lusvormig onderdeel van een verkeersdetector.
- `weerstation`: Een weerstation is een verzameling instrumenten die het weer kunnen meten.
- `flitser`: Een flitser bevat een mechanisme om een snelheidsmeting uit te voeren om snelheidsovertredingen in het verkeer te kunnen vaststellen.
- `waterstandmeter`: Een meter die de waterstand, over het algemeen ten opzichte van NAP, meet.
- `windmeter`: Apparatuur waarmee de snelheid en de richting van de wind kan worden gemeten.
- `lichtcel`: Lichtcel waarmee het verlichtingsniveau naar een lager verlichtingsniveau omgeschakeld wordt (dimmen) wanneer de situatie dit toelaat.
- `GMS sensor`: Gladheidsmeldsysteem (GMS) waarmee de kans op gladheid wordt voorspeld aan de hand van meting en interpretatie van de parameters die een rol spelen bij het ontstaan van gladheid.
- `radar detector`: Met een radardetector wordt het verkeer gedetecteerd, bijvoorbeeld voor het beïnvloeden van verkeerslichten.
