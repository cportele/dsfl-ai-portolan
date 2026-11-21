# BegroeidTerreindeel (bgt/topografie/begroeidterreindeel)

De collectie `begroeidterreindeel` van de API https://bag.ldproxy.net/bgt als één bestand, `begroeidterreindeel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair), `kruinlijn`; CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie, kruinlijn)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/begroeidterreindeel/begroeidterreindeel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Kleinste functioneel onafhankelijk stukje van een terrein dat er binnen het objecttype Terrein van NEN 3610 wordt onderscheiden, met aaneengesloten vegetatie. English: vegetated land: grass, forest, shrubs, green space, farmland (land cover surface).

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtFysiekVoorkomen (waardelijst FysiekVoorkomenBegroeidTerrein; BGT, authentiek)

- `loofbos`: Terreindeel begroeid met een dusdanige aantal loofbomen dat deze een min of meer gesloten geheel vormen of, na volgroeiing van de bomen, zullen vormen.
- `gemengd bos`: Terreindeel begroeid met een dusdanige aantal naald- en loofbomen dat deze een min of meer gesloten geheel vormen of, na volgroeiing van de bomen, zullen vormen.
- `naaldbos`: Terreindeel begroeid met een dusdanige aantal naaldbomen dat deze een min of meer gesloten geheel vormen of, na volgroeiing van de bomen, zullen vormen.
- `heide`: Terreindeel overwegend begroeid met heide en heideachtige vegetaties.
- `struiken`: Terreindeel bedekt met niet-gecultiveerde (natuurlijke), lage, houtachtige, overblijvende planten gekenmerkt door verschillende vertakkingen dicht bij de wortel en afwezigheid van opvallende stammen.
- `houtwal`: Terreindeel zijnde een afscheiding met beperkte breedte en beplant met bomen of struiken.
- `duin`: Verhoging of heuvel van zand of fijne losse aarde en verpulverd gesteente opgeworpen door wind of door stromend water.
- `grasland overig`: Terreindeel met een vegetatie bestaande uit grassen en of grasachtigen, en met de in graslanden voorkomende kruiden, dat niet in gebruik is voor agrarische doeleinden.
- `moeras`: Terreindeel met moerasvegetatie in stilstaand water van geringe diepte zonder merkbare toe- of afvloeiing.
- `rietland`: Terreindeel overwegend begroeid met rietvegetatie.
- `kwelder`: Buitendijks gelegen aangeslibd land van een wad, dat bij gewone vloed niet meer onder loopt.
- `fruitteelt`: Terreindeel begroeid met fruitbomen in de vorm van hoogstam en laagstamboomgaard, druiven of kleinfruit.
- `boomteelt`: Grond in gebruik voor het kweken van jonge siergewassen, bomen enz. ten behoeve van een later gebruik elders.
- `bouwland`: Terreindeel in gebruik als akker, met gewassen die in een teelt roulatieschema zijn opgenomen. Kan tijdelijk zonder gewas zijn of braak liggen.
- `grasland agrarisch`: Terreindeel met een vegetatie bestaande uit grassen en of grasachtigen, en met de in graslanden voorkomende kruiden, zijnde cultuurgrasland dat in gebruik is voor de veeteelt, bijvoorbeeld als weiland of als hooiland.
- `groenvoorziening`: Terreindeel met aangelegde beplanting, meestal gras, heesters of struiken.

`transitie` komt in de gegevens voor, maar staat niet in de waardelijsten; een definitie is niet gepubliceerd.

### plusFysiekVoorkomen (waardelijst FysiekVoorkomenBegroeidTerreinPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `akkerbouw`: Terreindeel in gebruik als akker, voor de teelt van akkerbouwgewassen.
- `braakliggend`: Terrein in gebruik als akker, maar tijdelijk niet beteeld met een landbouwgewas.
- `vollegrondsteelt`: Terreindeel in gebruik als akker, voor de teelt van tuinbouwgewassen.
- `bollenteelt`: Terreindeel in gebruik als akker, voor de teelt van bloembollen.
- `bosplantsoen`: Opgaande beplanting van houtachtige gewassen die struikvormend en/of boomvormend zijn. De soorten zijn als bosplantsoen opgekweekt en aangeplant.De beplanting kan open of gesloten zijn en bestaat vaak uit inheemse soorten. Onderscheidt zich van heesters omdat de sierkenmerken niet voorop staan.
- `gras- en kruidachtigen`: (Grond met) een laagblijvende, aaneengesloten kruidachtige vegetatie.
- `planten`: Beheerde niet nader gespecificeerde beplanting van groenvak in de openbare ruimte.
- `struikrozen`: Beheerde beplanting van groenvak in de openbare ruimte, zijnde in struikvorm groeiende rozen.
- `heesters`: Beplanting van houtige gewassen die struikvormend zijn en die al dan niet een gesloten geheel vormen. Het accent ligt op de sierwaarde, de beplanting kan uit één soort of uit meerdere soorten bestaan. Onder de heesters kan een houtachtige of kruidachtige onderbegroeiing aanwezig zijn. Het oppervlak met struikachtige gewassen is meer dan 50% van de totale oppervlakte van het vak.
- `bodembedekkers`: Beheerde beplanting van groenvak in de openbare ruimte, zijnde bodembedekkers.
- `laagstam boomgaarden`: Terreindeel begroeid met laagstamfruitbomen.
- `hoogstam boomgaarden`: Terreindeel begroeid met hoogstamfruitbomen.
- `wijngaarden`: Terreindeel begroeid met druivenstokken voor wijnbouw.
- `klein fruit`: Terreindeel begroeid met heesters voor zachtfruit zoals bessen of frambozen.
- `griend en hakhout`: Terreindeel met opgaande begroeiing van loofbomen, in een dicht groeiverband, en die periodiek wordt afgezet.
- `open duinvegetatie`: Duin met een overwegend grasachtige vegetatie.
- `gesloten duinvegetatie`: Duin met een overwegend opgaande vegetatie van struiken en of bomen.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
