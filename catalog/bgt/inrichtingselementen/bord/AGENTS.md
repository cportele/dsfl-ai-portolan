# Bord (bgt/inrichtingselementen/bord)

De collectie `bord` van de API https://bag.ldproxy.net/bgt als één bestand, `bord.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/bord/bord.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Een paneel waarop informatie wordt afgebeeld. English: sign: traffic sign, street name sign, information board (point).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeBordPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `informatiebord`: Een bord met daarop specifieke actuele informatie, zoals plattegronden of vertrektijden.
- `plaatsnaambord`: Een bord waarop een naam van een (woon)plaats of locatie is vermeld.
- `straatnaambord`: Bord waarop de door de gemeente vastgestelde naam van de straat is vermeld. Bord kan zich op een paal of aan de gevel bevinden.
- `verkeersbord`: Bord waarop een verkeersteken is aangebracht en waarvan de uitvoering wettelijk is voorgeschreven volgens het 'Reglement verkeersregels en verkeerstekens 1990 (RVV 1990)'.
- `scheepvaartbord`: Bord waarop een scheepvaartteken is aangebracht en waarvan de uitvoering als richtlijn is voorgeschreven volgens 'Richtlijnen Scheepvaarttekens (RST 2008)'.
- `verklikker transportleiding`: Bovengrondse voorziening om een ondergrondse transportleiding te markeren.
- `reclamebord`: Vrijstaand bord/zuil waarop rondom of aan één of meer zijden affiches kunnen worden (of zijn) geplakt.
- `wegwijzer`: Constructie voorzien van een of meer panelen met informatie ten behoeve van de bewegwijzering.
- `waarschuwingshek`: Constructie in de vorm van een hek, voorzien van rode en witte blokken of chevrons, die het verkeer attendeert op een gevarenpunt.
- `dynamische snelheidsindicator`: Een snelheidsinformatiebord dat in "real time" de snelheid van de weggebruikers aanduidt.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
