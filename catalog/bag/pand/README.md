# Pand (BAG)

Een pand is de kleinste, bij de totstandkoming functioneel en bouwkundig-constructief zelfstandige eenheid die direct en duurzaam met de aarde is verbonden en betreedbaar en afsluitbaar is. Een pand heeft zelf geen adres; de verblijfsobjecten in het pand (verblijfsobject.maaktDeelUitVan) hebben een adres. Een pand kan nul, één of meer verblijfsobjecten bevatten. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [pand](https://bag.ldproxy.net/bag/collections/pand) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.31049244020411, 52.108465652393924, 5.483953432605811, 52.21591997359349]

## Temporal Coverage

- **Start**: 1828-10-26T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | De unieke aanduiding van een pand. De identificatie bestaat uit 16 cijfers: de viercijferige gemeentecode van de gemeente die de identificatie heeft toegekend, de tweecijferige objecttypecode en een tiencijferig objectvolgnummer. De gemeentecode in de identificatie zegt niets over de gemeente waarin het object nu ligt. De identificatie verandert niet zolang het object bestaat; alle voorkomens (versies) van een object hebben dezelfde identificatie. |
| oorspronkelijkBouwjaar | int32 | De aanduiding van het jaar waarin een pand oorspronkelijk als bouwkundig gereed is of zal worden opgeleverd. Bij het opvoeren van een pand maakt de gemeente een reële inschatting van het waarschijnlijke bouwjaar; latere verbouwingen wijzigen het bouwjaar niet. De waarde 9999 betekent in de praktijk 'onbekend' (niet officieel gedocumenteerd); ook andere onwaarschijnlijke jaren komen voor. Bij oude panden is het bouwjaar vaak een schatting op een rond jaartal (1800, 1750, 1700, 1600), zodat aantallen per bouwjaar voor ongeveer 1900 slechts een grove indicatie zijn. |
| status | string | De fase van de levenscyclus van een pand waarin het betreffende pand zich bevindt. De BAG bevat gegevens over daadwerkelijk aanwezige, nog tot stand te brengen en verdwenen panden. Toegestane waarden: 'Bouwvergunning verleend': Een nieuw pand dat nog niet is gebouwd maar waarvoor wel een vergunning of andere publiekrechtelijke toestemming is verleend. 'Niet gerealiseerd pand': Een pand waarvoor een vergunning of andere publiekrechtelijke toestemming was verleend, maar waarvan is vastgesteld dat wordt afgezien van de bouw of waarvan de vergunning is ingetrokken. 'Bouw gestart': Een vergund pand waarvan is gemeld of vastgesteld dat de bouw is gestart (minimaal de aanleg van de fundering). 'Pand in gebruik (niet ingemeten)': Een pand dat in gebruik is genomen of gebruiksgereed is, maar waarvan de definitieve geometrie nog niet is ingemeten. 'Pand in gebruik': Een pand dat in gebruik is en waarvan de definitieve geometrie is ingemeten. 'Sloopvergunning verleend': Een pand waarvoor een vergunning tot sloop is verleend. 'Pand gesloopt': Een pand waarvan is gemeld of vastgesteld dat het is gesloopt; de bouwkundige constructie is verdwenen. 'Pand buiten gebruik': Een pand dat in dusdanige bouwkundige staat verkeert dat het daardoor redelijkerwijs niet te gebruiken is. 'Verbouwing pand': Een pand waarvoor een vergunning of andere publiekrechtelijke toestemming tot verbouw is verleend en waarbij de verbouwing nog niet is voltooid. 'Pand ten onrechte opgevoerd': Een pand dat niet had mogen worden opgenomen in de BAG-registratie en vervolgens is beëindigd. Eindstatussen (het object is beëindigd en de status kan niet meer wijzigen): 'Niet gerealiseerd pand', 'Pand gesloopt', 'Pand ten onrechte opgevoerd'. |
| geconstateerd | bool | Een aanduiding waarmee kan worden aangegeven dat een pand in de registratie is opgenomen als gevolg van een feitelijke constatering, zonder dat er op het moment van opname sprake was van een regulier brondocument voor deze opname. Het gaat bijvoorbeeld om panden die niet eerder in de registratie zijn opgenomen vanwege het ontbreken van de benodigde vergunning. In de BAG een indicatie J/N; hier `true` (J) of `false` (N). Basisgegeven, niet authentiek. |
| documentdatum | date32[day] | De datum waarop het brondocument is vastgesteld op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een pand heeft plaatsgevonden. |
| documentnummer | string | De unieke aanduiding van het brondocument op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een pand heeft plaatsgevonden binnen een gemeente. Maximaal 40 tekens. |
| gemeentecode | string | Code van de gemeente waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld 0307. Geen BAG-gegeven. |
| wijkcode | string | Code van de wijk waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld WK030701. Geen BAG-gegeven. |
| buurtcode | string | Code van de buurt waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld BU03070100. Geen BAG-gegeven. |
| gemeentenaam | string | Naam van de gemeente waarin het object ligt (zie gemeentecode), uit de CBS Wijk- en Buurtkaart 2026. Geen BAG-gegeven. |
| wijknaam | string | Naam van de wijk waarin het object ligt (zie wijkcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de wijkcode, samen met de naam. Geen BAG-gegeven. |
| buurtnaam | string | Naam van de buurt waarin het object ligt (zie buurtcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de buurtcode, samen met de naam. Geen BAG-gegeven. |
| grondoppervlakte | int32 | De oppervlakte van het bovenaanzicht van het pand (de geometrie) in gehele vierkante meters, berekend uit de geometrie in het Rijksdriehoeksstelsel, voor elke versie uit de geometrie van die versie. Niet de gebruiksoppervlakte van de verblijfsobjecten. Helpt hoofdgebouwen te onderscheiden van bijgebouwen zoals schuren en garages. Geen BAG-gegeven. |
| aantalVerblijfsobjecten | int64 | Het aantal verblijfsobjecten in het pand (verblijfsobject.maaktDeelUitVan), in de versies die geldig waren op de laatste dag van deze versie van het pand (bij de actuele versie: vandaag), ook verblijfsobjecten die nog gebouwd worden ('Verblijfsobject gevormd'), maar niet 'Verblijfsobject ingetrokken', 'Niet gerealiseerd verblijfsobject', 'Verblijfsobject ten onrechte opgevoerd'. Een pand zonder verblijfsobjecten, bijvoorbeeld een schuur, heeft 0. Geen BAG-gegeven. |
| voorkomenidentificatie | int32 | Volgnummer van dit voorkomen (deze versie) van het pand. De identificatie en de voorkomenidentificatie samen bepalen een unieke versie van een object. Het nummer begint bij 1 en wordt bij elke nieuwe versie opgehoogd; nummers van versies die niet in deze gegevens zijn opgenomen (zie beginGeldigheid) ontbreken. |
| beginGeldigheid | date32[day] | De datum waarop deze versie van het pand geldig is in de werkelijkheid conform de ingangsdatum in het brondocument. Als er geen expliciete ingangsdatum van geldigheid is opgenomen, wordt de datum van het brondocument overgenomen. De versies van een object sluiten naadloos op elkaar aan: de eindGeldigheid van een versie is de beginGeldigheid van de volgende. Versies die op dezelfde dag weer zijn vervangen (beginGeldigheid = eindGeldigheid) en inactieve of niet-BAG-voorkomens zijn in deze gegevens niet opgenomen. |
| eindGeldigheid | date32[day] | De datum waarop de periode van geldigheid van deze versie van het pand eindigt, bijvoorbeeld als gevolg van de vaststelling van een nieuw brondocument. Geldig tot (niet tot en met) deze datum. Leeg als de versie nog geldig is. Een object dat niet meer bestaat heeft een versie met een eindstatus (zie status) en zonder eindGeldigheid. |
| tijdstipRegistratie | timestamp[us] | Het tijdstip waarop deze versie van het pand is geregistreerd in de registratie van de bronhouder (gemeente) en daarmee authentiek is gemaakt. |
| eindRegistratie | timestamp[us] | Het tijdstip waarop deze versie van het pand is beëindigd in de registratie van de bronhouder. Een versie krijgt een eindRegistratie op het moment dat zij een eindGeldigheid krijgt; het is het tijdstipRegistratie van de volgende versie. Leeg als de versie nog niet is beëindigd. |
| tijdstipRegistratieLV | timestamp[us] | Het tijdstip waarop deze versie van het pand is opgenomen in de registratie van de landelijke voorziening (LV BAG). De gegevens zijn vanaf dat moment beschikbaar voor afnemers. |
| tijdstipEindRegistratieLV | timestamp[us] | Het tijdstip waarop de beëindiging van deze versie van het pand is opgenomen in de landelijke voorziening (LV BAG). Leeg als de versie nog niet is beëindigd. |
| voorgaandeVersie | date32[day] | De beginGeldigheid van de voorgaande versie van het pand; leeg bij de eerste versie. |
| volgendeVersie | date32[day] | De beginGeldigheid van de volgende versie van het pand; leeg bij de laatste versie. |
| geometrie | binary | De minimaal tweedimensionale geometrische representatie van het bovenzicht van de omtrekken van een pand. In de BAG met hoogte 0 geleverd; hier tweedimensionaal. Coördinaten in het Rijksdriehoeksstelsel (RD, EPSG:28992), in meter met maximaal drie decimalen; tweedimensionaal opgeslagen. |
| geometrie_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> | Bounding box van geometrie (GeoParquet covering), om bij een ruimtelijke selectie rijgroepen over te slaan. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./pand.parquet | 13.3 MB | 12202438b9f8... |
| ./thumbnail.png | 270.1 KB | 1220979043c9... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet")
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
