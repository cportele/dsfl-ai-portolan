# Verblijfsobject (BAG)

Een verblijfsobject is de kleinste binnen een of meer panden gelegen en voor woon-, bedrijfsmatige, of recreatieve doeleinden geschikte eenheid van gebruik die ontsloten wordt via een eigen afsluitbare toegang vanaf de openbare weg, een erf of een gedeelde verkeersruimte, onderwerp kan zijn van goederenrechtelijke rechtshandelingen en in functioneel opzicht zelfstandig is. Bijvoorbeeld een woning, winkel of kantoor. Een verblijfsobject is een adresseerbaar object: het heeft een hoofdadres (heeftAlsHoofdadres) en eventueel nevenadressen. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [verblijfsobject](https://bag.ldproxy.net/bag/collections/verblijfsobject) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.3165216186250905, 52.117692447248736, 5.483841323094554, 52.2158605967245]

## Temporal Coverage

- **Start**: 1828-10-26T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | De unieke aanduiding van een verblijfsobject. De identificatie bestaat uit 16 cijfers: de viercijferige gemeentecode van de gemeente die de identificatie heeft toegekend, de tweecijferige objecttypecode en een tiencijferig objectvolgnummer. De gemeentecode in de identificatie zegt niets over de gemeente waarin het object nu ligt. De identificatie verandert niet zolang het object bestaat; alle voorkomens (versies) van een object hebben dezelfde identificatie. |
| gebruiksdoel | list<element: string> | Een categorisering van de gebruiksdoelen van het verblijfsobject zoals in de vergunning of andere publiekrechtelijke toestemming is opgenomen of bij constatering is vastgesteld, conform de gebruiksfuncties van het Bouwbesluit 2012. Niet te verwarren met de planologische bestemming of het feitelijk gebruik. Eén of meer waarden. Toegestane waarden: 'woonfunctie': gebruiksfunctie voor het wonen 'bijeenkomstfunctie': gebruiksfunctie voor het samenkomen van personen voor kunst, cultuur, godsdienst, communicatie, kinderopvang, het verstrekken van consumpties voor het gebruik ter plaatse of het aanschouwen van sport 'celfunctie': gebruiksfunctie voor dwangverblijf van personen 'gezondheidszorgfunctie': gebruiksfunctie voor medisch onderzoek, verpleging, verzorging of behandeling 'industriefunctie': gebruiksfunctie voor het bedrijfsmatig bewerken of opslaan van materialen en goederen, of voor agrarische doeleinden 'kantoorfunctie': gebruiksfunctie voor administratie 'logiesfunctie': gebruiksfunctie voor het bieden van recreatief verblijf of tijdelijk onderdak aan personen 'onderwijsfunctie': gebruiksfunctie voor het geven van onderwijs 'sportfunctie': gebruiksfunctie voor het beoefenen van sport 'winkelfunctie': gebruiksfunctie voor het verhandelen van materialen, goederen of diensten 'overige gebruiksfunctie': niet benoemde gebruiksfunctie voor activiteiten waarbij het verblijven van personen een ondergeschikte rol speelt, bijvoorbeeld een garagebox. |
| oppervlakte | int32 | De gebruiksoppervlakte van een verblijfsobject in gehele vierkante meters, bepaald volgens NEN 2580; gemeenschappelijke ruimten tellen niet mee. Oppervlakten kleiner dan 1 m² worden afgerond op 1 m². De waarde 999999 komt voor en is geen werkelijke oppervlakte (niet officieel gedocumenteerd). |
| heeftAlsHoofdadres | string | De unieke aanduiding van de nummeraanduiding die in het kader van de Basisregistratie Adressen en Gebouwen is aangemerkt als het hoofdadres van het verblijfsobject. Een adresseerbaar object heeft precies één hoofdadres. Het volledige adres bestaat uit de naam van de openbare ruimte (nummeraanduiding.ligtAan), huisnummer, huisletter, huisnummertoevoeging, postcode en de naam van de woonplaats (nummeraanduiding.ligtIn, anders openbareruimte.ligtIn). Verwijst naar identificatie in de collectie bag/nummeraanduiding. |
| heeftAlsNevenadres | list<element: string> | De unieke aanduiding van de nummeraanduidingen die in het kader van de Basisregistratie Adressen en Gebouwen zijn aangemerkt als nevenadres van het verblijfsobject. Een nevenadres is een aanvullend adres, bijvoorbeeld voor een leveranciersingang; het duidt niet een gedeelte van het object aan. Meestal leeg. Verwijst naar identificatie in de collectie bag/nummeraanduiding. |
| maaktDeelUitVan | list<element: string> | De unieke aanduidingen van de panden waarvan het verblijfsobject onderdeel uitmaakt. In de meeste gevallen één pand, soms meerdere. De administratieve relatie is leidend boven de ruimtelijke ligging. Verwijst naar identificatie in de collectie bag/pand. |
| status | string | De fase van de levenscyclus van een verblijfsobject waarin het betreffende verblijfsobject zich bevindt. De BAG bevat gegevens over daadwerkelijk aanwezige, nog tot stand te brengen en verdwenen verblijfsobjecten. Toegestane waarden: 'Verblijfsobject gevormd': Een nieuw verblijfsobject in een nog niet gebouwd pand waarvoor een vergunning of andere publiekrechtelijke toestemming is verleend, of dat wordt gerealiseerd in een reeds bestaand pand. 'Niet gerealiseerd verblijfsobject': Een verblijfsobject waarvan is vastgesteld dat wordt afgezien van de bouw of waarvan de vergunning is ingetrokken. 'Verblijfsobject in gebruik (niet ingemeten)': Een verblijfsobject dat in gebruik is genomen of gebruiksgereed is, maar waarvan de definitieve geometrie nog niet is ingemeten. 'Verblijfsobject in gebruik': Een verblijfsobject dat in gebruik is en waarvan de definitieve geometrie is ingemeten. 'Verblijfsobject ingetrokken': Een verblijfsobject dat als zodanig opgehouden heeft te bestaan, bijvoorbeeld na sloop. 'Verblijfsobject buiten gebruik': Een verblijfsobject in een pand dat in dusdanige bouwkundige staat verkeert dat het daardoor redelijkerwijs niet te gebruiken is. 'Verbouwing verblijfsobject': Een verblijfsobject waarvoor een vergunning of andere publiekrechtelijke toestemming tot verbouw is verleend en waarbij de verbouwing nog niet is voltooid. 'Verblijfsobject ten onrechte opgevoerd': Een verblijfsobject dat niet had mogen worden opgenomen in de BAG-registratie en vervolgens is beëindigd. Eindstatussen (het object is beëindigd en de status kan niet meer wijzigen): 'Niet gerealiseerd verblijfsobject', 'Verblijfsobject ingetrokken', 'Verblijfsobject ten onrechte opgevoerd'. |
| geconstateerd | bool | Een aanduiding waarmee kan worden aangegeven dat een verblijfsobject in de registratie is opgenomen als gevolg van een feitelijke constatering, zonder dat er op het moment van opname sprake was van een regulier brondocument voor deze opname. Het gaat bijvoorbeeld om verblijfsobjecten die niet eerder in de registratie zijn opgenomen vanwege het ontbreken van de benodigde vergunning of omdat geen vergunning nodig was. In de BAG een indicatie J/N; hier `true` (J) of `false` (N). Basisgegeven, niet authentiek. |
| documentdatum | date32[day] | De datum waarop het brondocument is vastgesteld op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een verblijfsobject heeft plaatsgevonden. |
| documentnummer | string | De unieke aanduiding van het brondocument op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een verblijfsobject heeft plaatsgevonden binnen een gemeente. Maximaal 40 tekens. |
| gemeentecode | string | Code van de gemeente waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld 0307. Geen BAG-gegeven. |
| wijkcode | string | Code van de wijk waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld WK030701. Geen BAG-gegeven. |
| buurtcode | string | Code van de buurt waarin het object ligt, volgens de CBS Wijk- en Buurtkaart 2026, bijvoorbeeld BU03070100. Geen BAG-gegeven. |
| gemeentenaam | string | Naam van de gemeente waarin het object ligt (zie gemeentecode), uit de CBS Wijk- en Buurtkaart 2026. Geen BAG-gegeven. |
| wijknaam | string | Naam van de wijk waarin het object ligt (zie wijkcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de wijkcode, samen met de naam. Geen BAG-gegeven. |
| buurtnaam | string | Naam van de buurt waarin het object ligt (zie buurtcode), uit de CBS Wijk- en Buurtkaart 2026. Wijk- en buurtnamen zijn alleen binnen een gemeente uniek; groepeer daarom op de buurtcode, samen met de naam. Geen BAG-gegeven. |
| bouwjaarPand | int32 | Het oorspronkelijk bouwjaar van het pand waarvan het verblijfsobject deel uitmaakt (maaktDeelUitVan), uit de versie van het pand die geldig was op de laatste dag van deze versie (bij de actuele versie: vandaag); bij meerdere panden het oudste bouwjaar. Zie oorspronkelijkBouwjaar van pand voor de betekenis van 9999 en van ronde jaartallen. Geen BAG-gegeven. |
| statusPand | string | De status van het pand waarvan het verblijfsobject deel uitmaakt (maaktDeelUitVan), uit de versie van het pand die geldig was op de laatste dag van deze versie (bij de actuele versie: vandaag); bij meerdere panden de status van het pand dat het minst ver is, in de volgorde 'Bouwvergunning verleend', 'Bouw gestart', 'Verbouwing pand', 'Pand in gebruik (niet ingemeten)', 'Pand in gebruik', 'Pand buiten gebruik', 'Sloopvergunning verleend', 'Pand gesloopt', 'Niet gerealiseerd pand', 'Pand ten onrechte opgevoerd'. Zo hoort een verblijfsobject in een pand met status 'Bouw gestart' bij de bouw, ook als het verblijfsobject zelf de status 'Verblijfsobject gevormd' heeft, net als verblijfsobjecten in panden waarvoor alleen een vergunning is verleend. Geen BAG-gegeven. |
| voorkomenidentificatie | int32 | Volgnummer van dit voorkomen (deze versie) van het verblijfsobject. De identificatie en de voorkomenidentificatie samen bepalen een unieke versie van een object. Het nummer begint bij 1 en wordt bij elke nieuwe versie opgehoogd; nummers van versies die niet in deze gegevens zijn opgenomen (zie beginGeldigheid) ontbreken. |
| beginGeldigheid | date32[day] | De datum waarop deze versie van het verblijfsobject geldig is in de werkelijkheid conform de ingangsdatum in het brondocument. Als er geen expliciete ingangsdatum van geldigheid is opgenomen, wordt de datum van het brondocument overgenomen. De versies van een object sluiten naadloos op elkaar aan: de eindGeldigheid van een versie is de beginGeldigheid van de volgende. Versies die op dezelfde dag weer zijn vervangen (beginGeldigheid = eindGeldigheid) en inactieve of niet-BAG-voorkomens zijn in deze gegevens niet opgenomen. |
| eindGeldigheid | date32[day] | De datum waarop de periode van geldigheid van deze versie van het verblijfsobject eindigt, bijvoorbeeld als gevolg van de vaststelling van een nieuw brondocument. Geldig tot (niet tot en met) deze datum. Leeg als de versie nog geldig is. Een object dat niet meer bestaat heeft een versie met een eindstatus (zie status) en zonder eindGeldigheid. |
| tijdstipRegistratie | timestamp[us] | Het tijdstip waarop deze versie van het verblijfsobject is geregistreerd in de registratie van de bronhouder (gemeente) en daarmee authentiek is gemaakt. |
| eindRegistratie | timestamp[us] | Het tijdstip waarop deze versie van het verblijfsobject is beëindigd in de registratie van de bronhouder. Een versie krijgt een eindRegistratie op het moment dat zij een eindGeldigheid krijgt; het is het tijdstipRegistratie van de volgende versie. Leeg als de versie nog niet is beëindigd. |
| tijdstipRegistratieLV | timestamp[us] | Het tijdstip waarop deze versie van het verblijfsobject is opgenomen in de registratie van de landelijke voorziening (LV BAG). De gegevens zijn vanaf dat moment beschikbaar voor afnemers. |
| tijdstipEindRegistratieLV | timestamp[us] | Het tijdstip waarop de beëindiging van deze versie van het verblijfsobject is opgenomen in de landelijke voorziening (LV BAG). Leeg als de versie nog niet is beëindigd. |
| voorgaandeVersie | date32[day] | De beginGeldigheid van de voorgaande versie van het verblijfsobject; leeg bij de eerste versie. |
| volgendeVersie | date32[day] | De beginGeldigheid van de volgende versie van het verblijfsobject; leeg bij de laatste versie. |
| geometrie | binary | De minimaal tweedimensionale geometrische representatie van een verblijfsobject. Meestal een punt binnen het pand; in enkele gevallen een vlak, zoals in de BAG geregistreerd. In de BAG met hoogte 0 geleverd (in een klein aantal historische versies met een foutieve hoogte); hier tweedimensionaal. Coördinaten in het Rijksdriehoeksstelsel (RD, EPSG:28992), in meter met maximaal drie decimalen; tweedimensionaal opgeslagen. |
| geometrie_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> | Bounding box van geometrie (GeoParquet covering), om bij een ruimtelijke selectie rijgroepen over te slaan. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./verblijfsobject.parquet | 9.3 MB | 1220dea25238... |
| ./thumbnail.png | 229.1 KB | 1220701ac2e0... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet")
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
