# Woonplaats (BAG)

Een woonplaats is een door het bevoegde gemeentelijke orgaan als zodanig aangewezen en van een naam voorzien gedeelte van het grondgebied van de gemeente. Elke openbare ruimte ligt in een woonplaats; de woonplaats is onderdeel van het adres. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [woonplaats](https://bag.ldproxy.net/bag/collections/woonplaats) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.306458635645041, 52.10838438725852, 5.484329664176055, 52.21915384787237]

## Temporal Coverage

- **Start**: 2008-04-15T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | De unieke aanduiding van een woonplaats, zoals opgenomen in de landelijke woonplaatsentabel: een viercijferige code (0001-9999) die door het Kadaster wordt toegekend. De identificatie verandert niet zolang het object bestaat; alle voorkomens (versies) van een object hebben dezelfde identificatie. |
| naam | string | De benaming van een door het gemeentebestuur aangewezen woonplaats. Maximaal 80 tekens. |
| status | string | De fase van de levenscyclus van een woonplaats waarin de betreffende woonplaats zich bevindt. De BAG bevat gegevens over zowel bestaande als opgeheven woonplaatsen. Toegestane waarden: 'Woonplaats aangewezen': Woonplaats is aangewezen door het bevoegd gezag of geconstateerd. 'Woonplaats ingetrokken': Woonplaats is ingetrokken door het bevoegd gezag. Eindstatussen (het object is beëindigd en de status kan niet meer wijzigen): 'Woonplaats ingetrokken'. |
| geconstateerd | bool | Een aanduiding waarmee kan worden aangegeven dat een woonplaats in de registratie is opgenomen als gevolg van een feitelijke constatering, zonder dat er op het moment van opname sprake was van een regulier brondocument voor deze opname. Het gaat bijvoorbeeld om door burgers aangebrachte woonplaatsbenamingen die binnen andere processen aan het licht zijn gekomen. In de BAG een indicatie J/N; hier `true` (J) of `false` (N). Basisgegeven, niet authentiek. |
| documentdatum | date32[day] | De datum waarop het brondocument is vastgesteld op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een woonplaats heeft plaatsgevonden. |
| documentnummer | string | De unieke aanduiding van het brondocument op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een woonplaats heeft plaatsgevonden binnen een gemeente. Maximaal 40 tekens. |
| gemeenteWoonplaatsRelatie | string | De gemeenten waartoe de woonplaats behoort of heeft behoord, met de periode van de relatie. Afgeleid door het Kadaster uit de gemeentetabel (Tabel 33) van het ministerie van BZK en meegeleverd met het BAG-extract; geen authentiek BAG-gegeven en geen onderdeel van de BAG. Het betreft alle perioden, onafhankelijk van de versie van de woonplaats. |
| voorkomenidentificatie | int32 | Volgnummer van dit voorkomen (deze versie) van de woonplaats. De identificatie en de voorkomenidentificatie samen bepalen een unieke versie van een object. Het nummer begint bij 1 en wordt bij elke nieuwe versie opgehoogd; nummers van versies die niet in deze gegevens zijn opgenomen (zie beginGeldigheid) ontbreken. |
| beginGeldigheid | date32[day] | De datum waarop deze versie van de woonplaats geldig is in de werkelijkheid conform de ingangsdatum in het brondocument. Als er geen expliciete ingangsdatum van geldigheid is opgenomen, wordt de datum van het brondocument overgenomen. De versies van een object sluiten naadloos op elkaar aan: de eindGeldigheid van een versie is de beginGeldigheid van de volgende. Versies die op dezelfde dag weer zijn vervangen (beginGeldigheid = eindGeldigheid) en inactieve of niet-BAG-voorkomens zijn in deze gegevens niet opgenomen. |
| eindGeldigheid | date32[day] | De datum waarop de periode van geldigheid van deze versie van de woonplaats eindigt, bijvoorbeeld als gevolg van de vaststelling van een nieuw brondocument. Geldig tot (niet tot en met) deze datum. Leeg als de versie nog geldig is. Een object dat niet meer bestaat heeft een versie met een eindstatus (zie status) en zonder eindGeldigheid. |
| tijdstipRegistratie | timestamp[us] | Het tijdstip waarop deze versie van de woonplaats is geregistreerd in de registratie van de bronhouder (gemeente) en daarmee authentiek is gemaakt. |
| eindRegistratie | timestamp[us] | Het tijdstip waarop deze versie van de woonplaats is beëindigd in de registratie van de bronhouder. Een versie krijgt een eindRegistratie op het moment dat zij een eindGeldigheid krijgt; het is het tijdstipRegistratie van de volgende versie. Leeg als de versie nog niet is beëindigd. |
| tijdstipRegistratieLV | timestamp[us] | Het tijdstip waarop deze versie van de woonplaats is opgenomen in de registratie van de landelijke voorziening (LV BAG). De gegevens zijn vanaf dat moment beschikbaar voor afnemers. |
| tijdstipEindRegistratieLV | timestamp[us] | Het tijdstip waarop de beëindiging van deze versie van de woonplaats is opgenomen in de landelijke voorziening (LV BAG). Leeg als de versie nog niet is beëindigd. |
| voorgaandeVersie | date32[day] | De beginGeldigheid van de voorgaande versie van de woonplaats; leeg bij de eerste versie. |
| volgendeVersie | date32[day] | De beginGeldigheid van de volgende versie van de woonplaats; leeg bij de laatste versie. |
| geometrie | binary | De tweedimensionale geometrische representatie van het vlak dat wordt gevormd door de omtrekken van een woonplaats. Een vlak (Polygon) of een multivlak (MultiPolygon), zoals in de BAG geregistreerd. Het grondgebied van een gemeente is volledig en zonder overlap ingedeeld in woonplaatsen. Coördinaten in het Rijksdriehoeksstelsel (RD, EPSG:28992), in meter met maximaal drie decimalen; tweedimensionaal opgeslagen. |
| geometrie_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> | Bounding box van geometrie (GeoParquet covering), om bij een ruimtelijke selectie rijgroepen over te slaan. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./woonplaats.parquet | 67.1 KB | 122008cb1388... |
| ./thumbnail.png | 19.7 KB | 1220bd27e3d1... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/woonplaats/woonplaats.parquet")
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
