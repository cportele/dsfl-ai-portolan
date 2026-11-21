# Pand (BGT)

Een PAND is de kleinste bij de totstandkoming functioneel en bouwkundig-constructief zelfstandige eenheid die direct en duurzaam met de aarde is verbonden en betreedbaar en afsluitbaar is. Met historie: een rij per versie van een object, sleutel identificatie en tijdstipRegistratie; de versies die nu in de registratie staan hebben geen eindRegistratie. Dezelfde eigenschappen als de collectie [pand](https://bag.ldproxy.net/bgt/collections/pand) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BGT](https://img.shields.io/badge/BGT-blue) ![IMGeo](https://img.shields.io/badge/IMGeo-blue) ![topografie](https://img.shields.io/badge/topografie-blue) ![grootschalige topografie](https://img.shields.io/badge/grootschalige_topografie-blue) ![wegdelen](https://img.shields.io/badge/wegdelen-blue) ![terreindelen](https://img.shields.io/badge/terreindelen-blue) ![waterdelen](https://img.shields.io/badge/waterdelen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![inrichtingselementen](https://img.shields.io/badge/inrichtingselementen-blue)

## Spatial Coverage

- **Bounding Box**: [5.316467055086407, 52.11747208342856, 5.483953432605811, 52.21587259430813]

## Temporal Coverage

- **Start**: 2015-06-02T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | Uniek identificatienummer voor het object dat onveranderlijk is zolang het object bestaat. Hier de lokaalID van de NEN3610-identificatie; De lokaalID bestaat uit de bronhoudercode van de bronhouder die het object heeft aangemaakt, een punt en een UUID van 32 hexadecimale tekens. Die bronhoudercode zegt niets over de huidige bronhouder (zie bronhouder) en de identificatie is uniek over alle collecties. De identificatie is de id van het object (feature id); alle versies van een object hebben dezelfde identificatie. |
| identificatieBAGPND | string | De unieke identificatie van het object zoals is toegekend in de BAG-administratie. BGT, authentiek in een andere basisregistratie. De BAG-gegevens zijn die van de versie die geldig was op de laatste dag van deze BGT-versie (bij de actuele versie: vandaag). Verwijst naar identificatie in de collectie bag/pand. |
| nummeraanduidingreeks | string | Bevat de reeks nummeraanduidingen behorend bij het pand ten behoeve van visualisatie. Een reeks is het huisnummer of de reeks huisnummers (bijvoorbeeld '1-15') die op de kaart bij het pand staat, met de verblijfsobjecten in de BAG met het laagste en het hoogste huisnummer. BGT, authentiek. |
| objectBeginTijd | date32[day] | Datum waarop het object bij de bronhouder is ontstaan. Deze datum moet altijd gelijk zijn aan de datum uit de tijdstipregistratie van het eerste voorkomen van het object. De objectBeginTijd is bij alle versies van een object gelijk; een object dat opnieuw is ingemeten of gecorrigeerd behoudt zijn objectBeginTijd. De BGT legt de formele levensduur vast (in de registratie), niet de ouderdom in de werkelijkheid: een object dat bij de opbouw van de BGT (vanaf 2013) is opgenomen, kan veel ouder zijn. BGT, authentiek. |
| objectEindTijd | date32[day] | Datum waarop het object bij de bronhouder niet meer geldig is. Leeg zolang het object bestaat. BGT, authentiek. |
| tijdstipRegistratie | timestamp[us] | Tijdstip waarop deze instantie van het object is opgenomen door de bronhouder. Als een mutatie niet resulteert in een nieuw object, dan ontstaat een nieuwe versie van het object. In deze situatie verandert het tijdstipRegistratie van het object, terwijl de objectBeginTijd gelijk blijft. Begin van de periode waarin deze versie in de registratie stond. De versies van een object sluiten naadloos op elkaar aan: de eindRegistratie van een versie is het tijdstipRegistratie van de volgende. Lokale tijd (Europe/Amsterdam). BGT, authentiek. |
| eindRegistratie | timestamp[us] | Eind van de periode waarop deze instantie van het object geldig is bij de bronhouder. Wanneer deze waarde niet is ingevuld is de instantie nog geldig. Leeg als de versie nog geldig is. Gevuld bij een nieuwe versie (met het tijdstipRegistratie van die versie) of bij het einde van het object (gelijk aan de objectEindTijd). BGT, authentiek. |
| lvPublicatiedatum | timestamp[us] | Tijdstip waarop deze instantie van het object is opgenomen in de Landelijke Voorziening. Het gegeven is optioneel omdat een nieuw object pas een LV-publicatiedatum krijgt als het voor de eerste keer wordt opgenomen in de Landelijke Voorziening. Voor en tijdens aanlevering van een nieuw object aan de Landelijke Voorziening ontbreekt dit gegeven nog. Het moment vanaf wanneer de versie voor afnemers beschikbaar was. Is een versie meer dan eens gepubliceerd (bijvoorbeeld opnieuw bij het einde van het object), dan de laatste publicatie. BGT, authentiek. |
| bronhouder | string | De bronhoudercode van het object. Een letter en vier cijfers: 'G' met de gemeentecode, 'P' met de provinciecode, 'W' met de waterschapscode of 'L' voor een landelijke organisatie, bijvoorbeeld G0307 (gemeente Amersfoort) of L0004 (ProRail). De namen staan in de codelijst bronhouder. BGT, authentiek. |
| inOnderzoek | bool | Een aanduiding waarmee wordt aangegeven dat een onderzoek wordt uitgevoerd naar de juistheid van een of meer gegevens van het betreffende object. `true` als een of meer gegevens van deze versie in onderzoek zijn, dus mogelijk niet juist. BGT, authentiek. |
| relatieveHoogteligging | int32 | Aanduiding voor de relatieve hoogte van het object. In deze gegevens van -1 tot en met 5. 0 is maaiveld, positief erboven (bijvoorbeeld 1 voor een brug), negatief eronder (bijvoorbeeld -1 voor een tunnel); bij overlappende objecten de volgorde van boven naar beneden. BGT, authentiek. |
| bgtStatus | string | De status gekoppeld aan de levenscyclus van een geo-object. Waarden: codelijst Status. BGT, authentiek. |
| plusStatus | string | De status gekoppeld aan de levenscyclus van een geo-object, indien dit een uitbreiding van de populatie betreft. Waarden: codelijst StatusPlus. Zonder bijhouding door de bronhouder 'geenWaarde'. IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt. |
| voorgaandeVersie | timestamp[us] | Het tijdstipRegistratie van de voorgaande versie van het object; leeg bij de eerste versie. |
| volgendeVersie | timestamp[us] | Het tijdstipRegistratie van de volgende versie van het object; leeg bij de laatste versie. |
| oppervlakte | double | De oppervlakte van het vlak in m² (op dm² afgerond), berekend uit de geometrie in het Rijksdriehoeksstelsel; bogen als bogen. Geen BGT-gegeven. |
| gemeentecode | string | Code van de gemeente waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld 0307. Geen BGT-gegeven. |
| wijkcode | string | Code van de wijk waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld WK030701. Geen BGT-gegeven. |
| buurtcode | string | Code van de buurt waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld BU03070100. Geen BGT-gegeven. |
| gemeentenaam | string | Naam van de gemeente waarin het object ligt (zie gemeentecode), uit de CBS Wijk- en Buurtkaart 2026. Geen BGT-gegeven. |
| wijknaam | string | Naam van de wijk waarin het object ligt (zie wijkcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de wijkcode, samen met de naam. Geen BGT-gegeven. |
| buurtnaam | string | Naam van de buurt waarin het object ligt (zie buurtcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de buurtcode, samen met de naam. Geen BGT-gegeven. |
| geometrie | binary | Vlakgeometrie grondvlak. Coördinaten in het Rijksdriehoeksstelsel (RD, EPSG:28992), in meter met maximaal drie decimalen; tweedimensionaal. Bogen (cirkelbogen in de BGT) blijven bogen in JSON-FG (`profile=jsonfg`: CircularString, CompoundCurve, CurvePolygon, MultiSurface); in GeoJSON en HTML worden ze door lijnstukken benaderd. |
| geometrie_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> | Bounding box van geometrie (GeoParquet covering), om bij een ruimtelijke selectie rijgroepen over te slaan. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./pand.parquet | 13.1 MB | 1220f5e418e0... |
| ./thumbnail.png | 233.6 KB | 1220e3f3bc77... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/topografie/pand/pand.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.pdok.nl/introductie/-/article/basisregistratie-grootschalige-topografie-bgt-](https://www.pdok.nl/introductie/-/article/basisregistratie-grootschalige-topografie-bgt-)

## Processing Notes

Geladen in PostgreSQL/PostGIS met de scripts van de repository dsfl-ai (https://github.com/cportele/dsfl-ai; scripts/load_bgt.py), de database achter de API https://bag.ldproxy.net/bgt. Per objecttype geëxporteerd met de scripts van https://github.com/cportele/dsfl-ai-portolan: gen_sql.py leidt de queries af uit de feature provider van ldproxy, zodat de kolommen de eigenschappen van de API zijn; export.py schrijft de bestanden met GDAL en sorteert ze met gpio langs een Hilbert-curve (GeoParquet 2.0). Bogen zijn benaderd door lijnstukken met een maximale afwijking van 1 mm. Kolommen met verwijzingen bevatten alleen de identificatie.

## Attribution

Bron: Basisregistratie Grootschalige Topografie (BGT), PDOK

## License

[CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.nl)

## Contact

Clemens Portele, interactive instruments GmbH <portele@interactive-instruments.de>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
