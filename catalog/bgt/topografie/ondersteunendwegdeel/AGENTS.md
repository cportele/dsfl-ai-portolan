# OndersteunendWegdeel (bgt/topografie/ondersteunendwegdeel)

De collectie `ondersteunendwegdeel` van de API https://bag.ldproxy.net/bgt als één bestand, `ondersteunendwegdeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair), `kruinlijn`; CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie, kruinlijn)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/ondersteunendwegdeel/ondersteunendwegdeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Een deel van de weg dat niet primair bedoeld is voor gebruik door het verkeer. English: auxiliary road part: traffic island, verge, road shoulder (surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtFunctie (waardelijst FunctieOndersteunendWegdeel; BGT, authentiek)

- `verkeerseiland`: Ondersteunend wegdeel van beperkte omvang, uitgevoerd als verhoging of wegmarkering, dat wordt omsloten door wegdelen en ten doel heeft verkeersstromen te scheiden.
- `berm`: Een strook grond langs een weg of spoorweg.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFunctie (waardelijst TypeOndersteunendWegdeelPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.

### bgtFysiekVoorkomen (waardelijst FysiekVoorkomenOndersteunendWegdeel; BGT, authentiek)

- `gesloten verharding`: Verharding bestaande uit een materiaal dat niet verwijderbaar is zonder definitieve destructie, zoals bijvoorbeeld bitumen, cement of kunststof.
- `open verharding`: Verharding gevormd door in verband aangebrachte elementen van beperkte afmetingen, zoals bijvoorbeeld klinkers en tegels.
- `half verhard`: Verharding bestaande uit een door verdichting gebonden materiaal, of onsamenhangend materiaal.
- `onverhard`: Wegdelen waar geen verharding of aaneengesloten vegetatie aanwezig is.
- `groenvoorziening`: Terreindeel met aangelegde beplanting, meestal gras, heesters of struiken.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFysiekVoorkomen (waardelijst FysiekVoorkomenOndersteunendWegdeelPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

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
- `bosplantsoen`: Opgaande beplanting van houtachtige gewassen die struikvormend en/of boomvormend zijn. De soorten zijn als bosplantsoen opgekweekt en aangeplant.De beplanting kan open of gesloten zijn en bestaat vaak uit inheemse soorten. Onderscheidt zich van heesters omdat de sierkenmerken niet voorop staan.
- `gras- en kruidachtigen`: (Grond met) een laagblijvende, aaneengesloten kruidachtige vegetatie.
- `planten`: Beheerde niet nader gespecificeerde beplanting van groenvak in de openbare ruimte.
- `struikrozen`: Beheerde beplanting van groenvak in de openbare ruimte, zijnde in struikvorm groeiende rozen.
- `heesters`: Beplanting van houtige gewassen die struikvormend zijn en die al dan niet een gesloten geheel vormen. Het accent ligt op de sierwaarde, de beplanting kan uit één soort of uit meerdere soorten bestaan. Onder de heesters kan een houtachtige of kruidachtige onderbegroeiing aanwezig zijn. Het oppervlak met struikachtige gewassen is meer dan 50% van de totale oppervlakte van het vak.
- `bodembedekkers`: Beheerde beplanting van groenvak in de openbare ruimte, zijnde bodembedekkers.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
