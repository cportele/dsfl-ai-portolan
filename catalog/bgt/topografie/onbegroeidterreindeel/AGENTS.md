# OnbegroeidTerreindeel (bgt/topografie/onbegroeidterreindeel)

De collectie `onbegroeidterreindeel` van de API https://bag.ldproxy.net/bgt als één bestand, `onbegroeidterreindeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair), `kruinlijn`; CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie, kruinlijn)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/onbegroeidterreindeel/onbegroeidterreindeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Kleinste functioneel onafhankelijk stukje van een terrein, dat er binnen het objecttype Terrein van NEN 3610 wordt onderscheiden, zonder aaneengesloten vegetatie. English: unvegetated land: yard, paved or unpaved area, sand (land cover surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtFysiekVoorkomen (waardelijst FysiekVoorkomenOnbegroeidTerrein; BGT, authentiek)

- `erf`: Terreindeel dat bij een pand of overig bouwwerk hoort, dat niet nader wordt ingewonnen en dat bestaat uit een mengvorm van begroeiing, verharding, en/of water.
- `gesloten verharding`: Verharding bestaande uit een materiaal dat niet verwijderbaar is zonder definitieve destructie, zoals bijvoorbeeld bitumen, cement of kunststof.
- `open verharding`: Verharding gevormd door in verband aangebrachte elementen van beperkte afmetingen, zoals bijvoorbeeld klinkers en tegels.
- `half verhard`: Verharding bestaande uit een door verdichting gebonden materiaal, of onsamenhangend materiaal.
- `onverhard`: Terreindeel waar geen verharding of aaneengesloten vegetatie aanwezig is, niet zijnde zand. Braakliggend valt hier wel onder.
- `zand`: Terreindeel dat grotendeels bedekt is met zand.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFysiekVoorkomen (waardelijst FysiekVoorkomenOnbegroeidTerreinPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `strand en strandwal`: Onbegroeide zandige kustvlakte op de overgang van zee met land. Staat onder invloed van het zeewater en de wind.
- `zandverstuiving`: Een gebied met zandige bodem waarvan delen van het gebied zonder vegetatie zijn, door invloed van wind.
- `asfalt`: Gesloten verharding bestaande uit asfaltbeton of andere met bitumen gebonden materialen.
- `cementbeton`: Gesloten verharding bestaande uit gewapend of ongewapend beton.
- `kunststof`: Synthetisch vervaardigd materiaal dat als verharding dient, zoals kunstgras of kunststof toplagen op atletiekbanen.
- `betonstraatstenen`: Verharding gemaakt van betonstraatstenen. Straatsteen die als goedkope vervanging van de gebakken klinkers is ontwikkeld.
- `gebakken klinkers`: Verharding gemaakt van straatbakstenen. Gebakken klinkers worden voornamelijk geproduceerd uit grondstof van eigen bodem \– de beddingen van onze rivieren.
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
