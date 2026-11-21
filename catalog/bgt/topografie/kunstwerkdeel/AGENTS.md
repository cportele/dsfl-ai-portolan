# Kunstwerkdeel (bgt/topografie/kunstwerkdeel)

De collectie `kunstwerkdeel` van de API https://bag.ldproxy.net/bgt als één bestand, `kunstwerkdeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/kunstwerkdeel/kunstwerkdeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Onderdeel van een civiel-technisch werk voor de infrastructuur van wegen, water, spoorbanen, waterkeringen en/of leidingen. English: civil engineering structure: lock, weir, pumping station, platform, jetty, culvert.

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtType (waardelijst TypeKunstwerk; BGT, authentiek)

- `hoogspanningsmast`: Metalen mast of stellage ter ondersteuning van geleidedraden voor het transport van elektriciteit met een hoog voltage.
- `gemaal`: Een kunstwerk in principe bedoeld om water van een laag peil naar een hoog peil te brengen.
- `perron`: Verhoogde constructie langs een spoorrail of tramrail voor het in- en uitstappen van passagiers of voor het laden en lossen van goederen.
- `sluisdeur`: Het beweegbare deel van een kunstmatige waterkering die de verbinding tussen twee wateren kan afsluiten of openstellen en daartoe van deuren of schuiven is voorzien.
- `strekdam`: Constructie in het water ter verdediging van de kust/oever.
- `steiger`: Vaste (niet drijvende) waterbouwkundige constructie voor het aanleggen van schepen en bedoeld om deze schepen vanaf de wal te laden en te lossen.
- `stuw`: Een constructie met een vaste drempel of een beweegbare klep, die dient om de waterstand boven- en benedenstrooms te regelen.
- `sluis`: Een kunstmatige, beweegbare waterkering die de verbinding tussen twee wateren kan afsluiten of openstellen en daartoe van deuren of schuiven is voorzien.
- `niet-bgt`: Het object is geen BGT object.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusType (waardelijst TypeKunstwerkPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `keermuur`: Een keermuur of keerwand is een stijf, grond- of waterkerend kunstwerk dat door een groot gewicht en een brede voet een grote standzekerheid kan bereiken. Een keermuur is meestal van gewapend beton, maar er kan ook ander materiaal gebruikt worden.
- `duiker`: Kunstwerk voor de waterhuishouding, bestaande uit een gesloten kokervormige constructie met een in- en uitstroomopening, niet de gehele waterbreedte beslaand en aangebracht onder een weg of spoorweg of in een dam.
- `faunavoorziening`: Voorziening bij een weg of spoorweg, niet zijnde een ecoduct, om de uit dat werk voortvloeiende negatieve gevolgen voor de fauna zoveel mogelijk te voorkomen of te beperken.
- `vispassage`: Een kunstmatige passage ten behoeve van de vistrek bij kunstwerken in wateren.
- `bodemval`: Sprong in de bodem van een waterloop.
- `coupure`: Een onderbreking in een waterkering voor de doorvoer van een weg of spoorweg, die bij extreme waterstanden afsluitbaar is.
- `ponton`: Drijvende, dichte bak, waarover soms een dek is gelegd.
- `voorde`: Een doorwaadbare, doorgaans verharde, plaats in de waterloop, die dient voor de oversteek van die waterloop.
- `overkluizing`: Een overkluizing is een civieltechnisch kunstwerk waarmee een weg een andere weg, een plein of een waterloop (kruiselings) overwelft. In het geval van een waterweg is er onder het bouwwerk (vaak) geen scheepvaart mogelijk, maar ligt het wateroppervlak nog wel vrij. Een overkluizing is te vergelijken met een brug, alleen bestaat de brug in dit geval vaak niet uit een wegdek maar uit een opstal. Anders gesteld: het maakt meestal geen deel uit van een weg.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
