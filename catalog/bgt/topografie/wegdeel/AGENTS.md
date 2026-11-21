# Wegdeel (bgt/topografie/wegdeel)

De collectie `wegdeel` van de API https://bag.ldproxy.net/bgt als één bestand, `wegdeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair), `kruinlijn`; CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie, kruinlijn)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/wegdeel/wegdeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Kleinste functioneel onafhankelijk stukje van een NEN 3610 Weg met gelijkblijvende, homogene eigenschappen en relaties en primair bedoeld voor gebruik door weg-, spoor- en vliegverkeer te land. English: road part: carriageway, footpath, cycle path, parking space, driveway, railway bed (surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtFunctie (waardelijst FunctieWeg; BGT, authentiek)

- `OV-baan`: Wegdeel dat uitsluitend is bestemd en gemarkeerd voor openbaar vervoer en afgescheiden is van de andere wegdelen niet uitsluitend door markering.
- `overweg`: Een gelijkvloerse kruising van een wegdeel en een wegdeel type ov-baan met spoor type trein of sneltram.
- `spoorbaan`: Gebaand gedeelte voor het verkeer over rails.
- `baan voor vliegverkeer`: Wegdeel uitsluitend bedoeld voor vliegverkeer.
- `rijbaan autosnelweg`: Wegdeel dat onderdeel is van een weg uitsluitend bestemd voor snelverkeer en met gescheiden rijbanen en ongelijkvloerse kruisingen.
- `rijbaan autoweg`: Wegdeel dat onderdeel is van een weg uitsluitend bestemd voor snelverkeer.
- `rijbaan regionale weg`: Wegdeel dat onderdeel is van een weg die een verbinding vormt tussen bewoonde oorden of tussen wijken binnen een dorp of stad waarbij er een, meestal fysieke, scheiding is tussen langzaam verkeer en snelverkeer.
- `rijbaan lokale weg`: Wegdeel dat onderdeel is van een weg van lokaal belang.
- `fietspad`: Weg uitsluitend bestemd voor fietsers en/of bromfietsers of een deel van een weg bestaande uit een oranjekleurige verhardingstrook met daarop een wit rijwielsymbool.
- `voetpad`: Wegdeel waar voetgangers gebruik van moeten maken.
- `voetpad op trap`: Voetpad op verkeersinfrastructurele voorziening bestaande uit een constructie van treden, waarop men een hoger of lager gelegen plaats kan bereiken.
- `ruiterpad`: Een wegdeel primair aangelegd voor het gebruik door ruiters.
- `parkeervlak`: Wegdeel bestemd voor het parkeren van motorvoertuigen.
- `voetgangersgebied`: Wegdeel alleen voor het gebruik door voetgangers, waarbij het door voetgangers te gebruiken gebied de volle breedte van de weg beslaat en het gebied een nadrukkelijk openbaar karakter heeft.
- `inrit`: Toegangswegen, oprijlanen en dergelijke met verkeersfunctie die leiden naar erven en terreinen.
- `woonerf`: Wegdeel waar de verblijfsfunctie (lopen, spelen, ontmoeten enzovoorts) prioriteit heeft boven de verkeersfunctie.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFunctie (waardelijst FunctieWegPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `verkeersdrempel`: Verhoging in een regionale rijbaan, bedoeld om het gemotoriseerde verkeer met een lage snelheid te laten rijden.
- `verbindingsweg`: Een verbindingsweg is (in principe) een eenrichtingsweg, gelegen binnen een knooppunt of aansluiting, die onderdeel is van de wijze waarop de ongelijkvloersheid is gerealiseerd.
- `calamiteitendoorsteek`: Een (Calamiteiten doorsteek) CADO heeft tot doel het verkeer op een rijbaan via een doorsteek van de weg te kunnen geleiden in geval van een calamiteit of werkzaamheden op de rijbaan. Een tweede doel is het faciliteren van toegang tot rijbanen voor hulpdiensten vanaf andere rijbanen of van een parallelweg.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.

### bgtFysiekVoorkomen (waardelijst FysiekVoorkomenWeg; BGT, authentiek)

- `gesloten verharding`: Verharding bestaande uit een materiaal dat niet verwijderbaar is zonder definitieve destructie, zoals bijvoorbeeld bitumen, cement of kunststof.
- `open verharding`: Verharding gevormd door in verband aangebrachte elementen van beperkte afmetingen, zoals bijvoorbeeld klinkers en tegels.
- `half verhard`: Verharding bestaande uit een door verdichting gebonden materiaal, of onsamenhangend materiaal.
- `onverhard`: Wegdelen waar geen verharding of aaneengesloten vegetatie aanwezig is.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFysiekVoorkomen (waardelijst FysiekVoorkomenWegPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `asfalt`: Gesloten verharding bestaande uit asfaltbeton of andere met bitumen gebonden materialen.
- `cementbeton`: Gesloten verharding bestaande uit gewapend of ongewapend beton.
- `betonstraatstenen`: Verharding gemaakt van betonstraatstenen. Straatsteen die als goedkope vervanging van de gebakken klinkers is ontwikkeld.
- `gebakken klinkers`: Verharding gemaakt van straatbakstenen. Gebakken klinkers worden voornamelijk geproduceerd uit grondstof van eigen bodem; de beddingen van onze rivieren.
- `tegels`: Bestrating van tegels, een platte vaak vierkante betonnen steen; veelal gebruikt voor trottoirbestrating.
- `sierbestrating`: Bestrating, uitgevoerd in verschillende bestratingsverbanden en -materialen, of in een sierverband, die vooral wordt toegepast uit esthetische overwegingen.
- `beton element`: Geprepareerde elementen van beton zoals, trottoirbanden, opsluitbanden en stelconplaten.
- `grasklinkers`: Elementenverharding bestaande uit elementen van beperkte afmetingen die ten behoeve van de doorgroei van grassen en kruiden, zijn voorzien van openingen of met tussenruimten aangebracht.
- `schelpen`: Ongebonden verharding bestaande uit schelpenmateriaal.
- `puin`: Puin is afvalmateriaal dat bestaat uit losse brokstukken, grotendeels bestaande uit stenen en beton, van gesloopte of ingestorte gebouwen, viaducten, bruggen en andere objecten.
- `grind`: Ongebonden verharding bestaande uit kiezelmateriaal, waarvan de stenen in doorsnede variëren van 1 tot 5 cm.
- `gravel`: Gravel is een ondergrond van gemalen baksteen die veel wordt gebruikt bij tennis en ook wel op atletiekbanen.
- `boomschors`: Onverhard met als deklaag boomschors.
- `zand`: Onverhard met als deklaag zand.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
