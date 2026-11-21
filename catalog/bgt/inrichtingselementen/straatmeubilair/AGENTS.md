# Straatmeubilair (bgt/inrichtingselementen/straatmeubilair)

De collectie `straatmeubilair` van de API https://bag.ldproxy.net/bgt als één bestand, `straatmeubilair.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/inrichtingselementen/straatmeubilair/straatmeubilair.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Een ruimtelijk object ter inrichting van de openbare ruimte. English: street furniture: bench, bicycle rack, playground equipment, bus shelter, letter box (point).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusType (waardelijst TypeStraatmeubilairPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `abri`: Overdekte wachtplaats voor passagiers van het openbaar vervoer.
- `bolder`: Een inrichting aan de wal, waar een schip, door middel van een tros of landvast, aan vastgelegd kan worden.
- `brievenbus`: Uitpandige kast waar post in kan worden gedeponeerd ter bezorging.
- `fietsenrek`: Een duurzaam verankerd rek in de openbare ruimte voor het stallen van fietsen.
- `kunstobject`: Een object dat als kunst gezien wordt en een bepaalde schoonheid heeft, niet door de natuur gemaakt.
- `openbaar toilet`: Voor mensen bedoeld toilet niet zijnde een pand, langs de openbare weg.
- `slagboom`: Boom of balk om de weg of een gedeelte hiervan af te sluiten.
- `speelvoorziening`: Aard en nagelvast met de grond verbonden constructie in de openbare ruimte, bedoeld als speelmateriaal voor kinderen.
- `telefooncel`: Niet-inpandige ruimte in openbaar gebied louter bestemd voor telefoneren.
- `bank`: Aaneengesloten zitplaats voor verscheidene personen, bedoeld voor openbaar gebruik en geplaatst in de openbare ruimte (vnl. in parken, plantsoenen, bossen en langs wegen).
- `picknicktafel`: Een `picknicktafel` is een tafel met vaak daaraan gemonteerde zitbanken of stoelen die kan gebruikt worden om te picknicken.
- `fontein`: Een fontein is een natuurlijke of kunstmatige installatie die water spuit.
- `lichtpunt`: Een lichtpunt is een lamp die licht uitzendt niet verbonden met een mast die het maaiveld raakt.
- `parkeerbeugel`: Een omklapbare beugel voor het afschermen van een parkeerplaats.
- `betaalautomaat`: Een apparaat dat betaalkaarten en/of contant geld accepteert om betalingen uit te voeren.
- `reclamezuil`: Vrijstaand bord/zuil waarop rondom of aan één of meer zijden affiches kunnen worden (of zijn) geplakt.
- `fietsenkluis`: Een fietskluis is een kluis om een fiets in te bewaren, meestal ter voorkoming van diefstal of beschadiging.
- `herdenkingsmonument`: Langs de weg of elders in het terrein aangelegd object ter herdenking van personen of evenementen.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
