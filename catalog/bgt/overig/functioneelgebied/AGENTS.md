# FunctioneelGebied (bgt/overig/functioneelgebied)

De collectie `functioneelgebied` van de API https://bag.ldproxy.net/bgt als één bestand, `functioneelgebied.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/overig/functioneelgebied/functioneelgebied.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Begrensd en benoemd gebied dat door een functionele eenheid beschreven wordt. English: functional area: dike (flood defence), playground, sports field, park, dog area.

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### bgtType (waardelijst TypeFunctioneelGebied; BGT, authentiek)

- `kering`: Een waterkerende en / of scheidende, kunstmatige of natuurlijke hoogte of hooggelegen gronden inclusief de daarin aanwezige waterkerende elementen.
- `niet-bgt`: Het object is geen BGT object.

### plusType (waardelijst TypeFunctioneelGebiedPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `bedrijvigheid`: Gebied waarop panden of overige gebouwen staan, en / of niet bebouwde oppervlakte , voornamelijk gebruikt voor economische activiteiten en non-profit activiteiten.
- `natuur en landschap`: Gebied dat wegens natuurschoon en/of natuurlijke historie in stand wordt gehouden.
- `landbouw`: Gebied primair in gebruik voor land- en tuinbouwproductie.
- `bewoning`: Gebied waarop panden of overige bouwwerken staan die voornamelijk gebruikt worden voor bewoning, inclusief erven en tuinen die bij de panden behoren.
- `infrastructuur verkeer en vervoer`: Gebied primair in gebruik voor verkeer en vervoer, waaronder verstaan spoorwegen, wegdelen, vliegverkeersbanen, parkeerterreinen, bermen en de ondersteunende objecten als kunstwerken.
- `infrastructuur waterstaatswerken`: Gebied grenzend aan oppervlaktewater, primair in gebruik voor de oppervlaktewaterhuishouding (waterafvoer, wateraanvoer en waterconservering).
- `waterbergingsgebied`: Terrein met als functie het tijdelijk of langdurig bergen van (regen)wateroverschotten uit de omgeving.
- `maatschappelijke en/of publieksvoorziening`: Bebouwd of landelijk gebied, niet zijnde woon- of bedrijventerrein, in gebruik voor maatschappelijke- en publieksdoeleinden (omvat overheids- en particuliere terreinen).
- `recreatie`: Gebied in gebruik voor openlucht recreatie.
- `begraafplaats`: Een besloten gebied waar lichamen van overleden personen worden begraven. Ook worden op begraafplaatsen urnen as van gecremeerde lichamen bewaard.
- `functioneel beheer`: Gebied waar een specifiek beheer voor benodigd is, louter bepaald vanuit beheer oogpunt.
- `recreatie: speeltuin`: Geheel van begroeiing, verharding, opstallen en speelwerktuigen, bedoeld als speelplaats voor kinderen.
- `recreatie: park`: Landschappelijk ingericht terrein, begroeid met houtachtige en kruidachtige vegetatie, verharding, objecten, waterpartijen en dergelijke, bedoeld als (grootschalige) recreatieve voorziening.
- `recreatie: sportterrein`: Terrein, mogelijk met groenvoorziening, verharding en bebouwing, bestemd voor sportbeoefening.
- `recreatie: camping`: Geheel van verharding, begroeiing en opstallen, in gebruik als terrein waar tijdelijk tenten en/of caravans kunnen worden geplaatst ten behoeve van recreatie.
- `recreatie: bungalowpark`: Geheel van verharding, begroeiing, overige opstallen en gebouwen, bedoeld als vakantie-/weekendhuisjes die niet permanent bewoond worden.
- `recreatie: volkstuin`: Terreingedeelte in gebruik als volkstuinen, inclusief bebouwing, verharding en dergelijke.
- `functioneel beheer: hondenuitlaatplaats`: Een uitlaatplaats waar uw hond zijn behoefte kan/ mag doen waarbij geen opruimplicht bestaat.
- `bushalte`: Halteplaats voor bussen van het openbaar vervoer.
- `carpoolplaats`: Parkeerplaats die qua ligging en ontsluiting geschikt is voor carpooling.
- `benzinestation`: Geheel van installaties, verharding en opstallen waar brandstoffen ten behoeve van verbrandingsmotoren worden verkocht.
- `verzorgingsplaats`: Langs de weg gelegen parkeergelegenheid, met inbegrip van de daarbij behorende verharde en onverharde banen en een of meer voorzieningen ten behoeve van reizigers en/of voertuigen.

Daarnaast als reden voor het ontbreken van een waarde: `waardeOnbekend`.
