# Standplaats (BAG)

Een standplaats is een door het bevoegde gemeentelijke orgaan als zodanig aangewezen terrein of gedeelte daarvan dat bestemd is voor het permanent plaatsen van een niet direct en niet duurzaam met de aarde verbonden en voor woon-, bedrijfsmatige, of recreatieve doeleinden geschikte ruimte, bijvoorbeeld een woonwagen of strandtent. Een standplaats is een adresseerbaar object. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [standplaats](https://bag.ldproxy.net/bag/collections/standplaats) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.3460331404618815, 52.13776674139658, 5.411849521383412, 52.193755964640296]

## Temporal Coverage

- **Start**: 1979-10-22T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | De unieke aanduiding van een standplaats. De identificatie bestaat uit 16 cijfers: de viercijferige gemeentecode van de gemeente die de identificatie heeft toegekend, de tweecijferige objecttypecode en een tiencijferig objectvolgnummer. De gemeentecode in de identificatie zegt niets over de gemeente waarin het object nu ligt. De identificatie verandert niet zolang het object bestaat; alle voorkomens (versies) van een object hebben dezelfde identificatie. |
| heeftAlsHoofdadres | string | De unieke aanduiding van de nummeraanduiding die in het kader van de Basisregistratie Adressen en Gebouwen is aangemerkt als het hoofdadres van de standplaats. Een adresseerbaar object heeft precies één hoofdadres. Het volledige adres bestaat uit de naam van de openbare ruimte (nummeraanduiding.ligtAan), huisnummer, huisletter, huisnummertoevoeging, postcode en de naam van de woonplaats (nummeraanduiding.ligtIn, anders openbareruimte.ligtIn). Verwijst naar identificatie in de collectie bag/nummeraanduiding. |
| heeftAlsNevenadres | list<element: string> | De unieke aanduiding van de nummeraanduidingen die in het kader van de Basisregistratie Adressen en Gebouwen zijn aangemerkt als nevenadres van de standplaats. Een nevenadres is een aanvullend adres, bijvoorbeeld voor een leveranciersingang; het duidt niet een gedeelte van het object aan. Meestal leeg. Verwijst naar identificatie in de collectie bag/nummeraanduiding. |
| status | string | De fase van de levenscyclus van een standplaats waarin de betreffende standplaats zich bevindt. De BAG bevat gegevens over zowel daadwerkelijk aanwezige als ingetrokken standplaatsen. Toegestane waarden: 'Plaats aangewezen': Plaats is aangewezen door het bevoegd gezag of geconstateerd. 'Plaats ingetrokken': Plaats is ingetrokken door het bevoegd gezag. Eindstatussen (het object is beëindigd en de status kan niet meer wijzigen): 'Plaats ingetrokken'. |
| geconstateerd | bool | Een aanduiding waarmee kan worden aangegeven dat een standplaats in de registratie is opgenomen als gevolg van een feitelijke constatering, zonder dat er op het moment van opname sprake was van een regulier brondocument voor deze opname. Het gaat bijvoorbeeld om het feitelijk gebruik van (een gedeelte van) een terrein dat binnen andere processen aan het licht is gekomen. In de BAG een indicatie J/N; hier `true` (J) of `false` (N). Basisgegeven, niet authentiek. |
| documentdatum | date32[day] | De datum waarop het brondocument is vastgesteld op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een standplaats heeft plaatsgevonden. |
| documentnummer | string | De unieke aanduiding van het brondocument op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een standplaats heeft plaatsgevonden binnen een gemeente. Maximaal 40 tekens. |
| gemeentecode | string | Code van de gemeente waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld 0307. Geen BAG-gegeven. |
| wijkcode | string | Code van de wijk waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld WK030701. Geen BAG-gegeven. |
| buurtcode | string | Code van de buurt waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld BU03070100. Geen BAG-gegeven. |
| gemeentenaam | string | Naam van de gemeente waarin het object ligt (zie gemeentecode), uit de CBS Wijk- en Buurtkaart 2026. Geen BAG-gegeven. |
| wijknaam | string | Naam van de wijk waarin het object ligt (zie wijkcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de wijkcode, samen met de naam. Geen BAG-gegeven. |
| buurtnaam | string | Naam van de buurt waarin het object ligt (zie buurtcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de buurtcode, samen met de naam. Geen BAG-gegeven. |
| voorkomenidentificatie | int32 | Volgnummer van dit voorkomen (deze versie) van de standplaats. De identificatie en de voorkomenidentificatie samen bepalen een unieke versie van een object. Het nummer begint bij 1 en wordt bij elke nieuwe versie opgehoogd; nummers van versies die niet in deze gegevens zijn opgenomen (zie beginGeldigheid) ontbreken. |
| beginGeldigheid | date32[day] | De datum waarop deze versie van de standplaats geldig is in de werkelijkheid conform de ingangsdatum in het brondocument. Als er geen expliciete ingangsdatum van geldigheid is opgenomen, wordt de datum van het brondocument overgenomen. De versies van een object sluiten naadloos op elkaar aan: de eindGeldigheid van een versie is de beginGeldigheid van de volgende. Versies die op dezelfde dag weer zijn vervangen (beginGeldigheid = eindGeldigheid) en inactieve of niet-BAG-voorkomens zijn in deze gegevens niet opgenomen. |
| eindGeldigheid | date32[day] | De datum waarop de periode van geldigheid van deze versie van de standplaats eindigt, bijvoorbeeld als gevolg van de vaststelling van een nieuw brondocument. Geldig tot (niet tot en met) deze datum. Leeg als de versie nog geldig is. Een object dat niet meer bestaat heeft een versie met een eindstatus (zie status) en zonder eindGeldigheid. |
| tijdstipRegistratie | timestamp[us] | Het tijdstip waarop deze versie van de standplaats is geregistreerd in de registratie van de bronhouder (gemeente) en daarmee authentiek is gemaakt. |
| eindRegistratie | timestamp[us] | Het tijdstip waarop deze versie van de standplaats is beëindigd in de registratie van de bronhouder. Een versie krijgt een eindRegistratie op het moment dat zij een eindGeldigheid krijgt; het is het tijdstipRegistratie van de volgende versie. Leeg als de versie nog niet is beëindigd. |
| tijdstipRegistratieLV | timestamp[us] | Het tijdstip waarop deze versie van de standplaats is opgenomen in de registratie van de landelijke voorziening (LV BAG). De gegevens zijn vanaf dat moment beschikbaar voor afnemers. |
| tijdstipEindRegistratieLV | timestamp[us] | Het tijdstip waarop de beëindiging van deze versie van de standplaats is opgenomen in de landelijke voorziening (LV BAG). Leeg als de versie nog niet is beëindigd. |
| voorgaandeVersie | date32[day] | De beginGeldigheid van de voorgaande versie van de standplaats; leeg bij de eerste versie. |
| volgendeVersie | date32[day] | De beginGeldigheid van de volgende versie van de standplaats; leeg bij de laatste versie. |
| geometrie | binary | De tweedimensionale geometrische representatie van de omtrekken van een standplaats. Coördinaten in het Rijksdriehoeksstelsel (RD, EPSG:28992), in meter met maximaal drie decimalen; tweedimensionaal opgeslagen. |
| geometrie_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> | Bounding box van geometrie (GeoParquet covering), om bij een ruimtelijke selectie rijgroepen over te slaan. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./standplaats.parquet | 25.2 KB | 1220ff2f486c... |
| ./thumbnail.png | 17.5 KB | 12200a9c7ae4... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/standplaats/standplaats.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.kadaster.nl/zakelijk/producten/adressen-en-gebouwen/bag-2.0-extract](https://www.kadaster.nl/zakelijk/producten/adressen-en-gebouwen/bag-2.0-extract)

## Processing Notes

Geladen in PostgreSQL/PostGIS met de scripts van de repository dsfl-ai (https://github.com/cportele/dsfl-ai; scripts/load_bag.py, scripts/finalize.sql), de database achter de API https://bag.ldproxy.net/bag. Per objecttype geëxporteerd met de scripts van https://github.com/cportele/dsfl-ai-portolan: gen_sql.py leidt de queries af uit de feature provider van ldproxy, zodat de kolommen de eigenschappen van de API zijn; export.py schrijft de bestanden met GDAL en sorteert ze met gpio langs een Hilbert-curve (GeoParquet 2.0). Bogen zijn benaderd door lijnstukken met een maximale afwijking van 1 mm. Kolommen met verwijzingen bevatten alleen de identificatie.

## Attribution

Bron: Kadaster, Basisregistratie Adressen en Gebouwen (BAG)

## License

[CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.nl)

## Contact

Clemens Portele, interactive instruments GmbH <portele@interactive-instruments.de>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
