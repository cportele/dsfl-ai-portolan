# Nummeraanduiding (BAG)

Een nummeraanduiding is een door het bevoegde gemeentelijke orgaan als zodanig toegekende aanduiding van een verblijfsobject, een standplaats of een ligplaats: het samenstel van postcode, huisnummer, huisletter en huisnummertoevoeging. Samen met de naam van de openbare ruimte en de naam van de woonplaats vormt de nummeraanduiding het officiële adres. Een nummeraanduiding heeft geen geometrie; de locatie is die van het adresseerbare object dat naar de nummeraanduiding verwijst. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [nummeraanduiding](https://bag.ldproxy.net/bag/collections/nummeraanduiding) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.306458635645041, 52.10838438725852, 5.484329664176055, 52.21915384787237]

## Temporal Coverage

- **Start**: 1984-01-31T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | De unieke aanduiding van een nummeraanduiding. De identificatie bestaat uit 16 cijfers: de viercijferige gemeentecode van de gemeente die de identificatie heeft toegekend, de tweecijferige objecttypecode en een tiencijferig objectvolgnummer. De gemeentecode in de identificatie zegt niets over de gemeente waarin het object nu ligt. De identificatie verandert niet zolang het object bestaat; alle voorkomens (versies) van een object hebben dezelfde identificatie. |
| huisnummer | int32 | Een door of namens het gemeentebestuur ten aanzien van een adresseerbaar object toegekende nummering. Een natuurlijk getal tussen 1 en 99999. |
| huisletter | string | Een door of namens het gemeentebestuur ten aanzien van een adresseerbaar object toegekende toevoeging aan een huisnummer in de vorm van een alfanumeriek teken: een hoofdletter (A-Z) of kleine letter (a-z). Hoofdlettergevoelig. |
| huisnummertoevoeging | string | Een door of namens het gemeentebestuur ten aanzien van een adresseerbaar object toegekende nadere toevoeging aan een huisnummer of een combinatie van huisnummer en huisletter. Maximaal vier tekens: hoofdletters, kleine letters en/of cijfers; de tekens '/' en '-' maken geen deel uit van de toevoeging. |
| postcode | string | De door PostNL vastgestelde code behorende bij een bepaalde combinatie van een straatnaam en een huisnummer: vier cijfers, waarvan het eerste niet 0 is, en twee hoofdletters, zonder spatie (bijvoorbeeld 3811LM). Basisgegeven, niet authentiek. Kan ontbreken als PostNL geen postcode heeft vastgesteld, bijvoorbeeld bij objecten met uitsluitend de gebruiksfunctie 'overige gebruiksfunctie'. Een postcode kan bij meerdere openbare ruimten horen; postcode en huisnummer samen (met huisletter en huisnummertoevoeging) duiden een adres aan. Niet elke postcode heeft een postcodegebied bij het CBS, bijvoorbeeld een postcode die na de peildatum van de CBS-gegevens is uitgegeven of al eerder is vervallen. Verwijst naar postcode in de collectie postcode6/postcode6. |
| typeAdresseerbaarObject | string | De aard van het object waaraan de nummeraanduiding is toegekend. Het object zelf vindt men in de betreffende collectie (verblijfsobject, standplaats of ligplaats) via de eigenschap heeftAlsHoofdadres of heeftAlsNevenadres. Toegestane waarden: 'Verblijfsobject': Nummeraanduiding is bedoeld voor een verblijfsobject. 'Standplaats': Nummeraanduiding is bedoeld voor een standplaats. 'Ligplaats': Nummeraanduiding is bedoeld voor een ligplaats. |
| ligtAan | string | De unieke aanduiding van de openbare ruimte waaraan het adresseerbare object is gelegen; de naam van de openbare ruimte is de straatnaam van het adres. Verwijst naar identificatie in de collectie bag/openbareruimte. |
| ligtIn | string | De unieke aanduiding van de woonplaats waarbinnen het object waaraan de nummeraanduiding is toegekend is gelegen. Alleen opgenomen als het object in een andere woonplaats ligt dan de openbare ruimte (ligtAan); dan gaat deze woonplaats voor. Meestal leeg: de woonplaats van het adres is dan de woonplaats van de openbare ruimte. Verwijst naar identificatie in de collectie bag/woonplaats. |
| status | string | De fase van de levenscyclus van een nummeraanduiding waarin de betreffende nummeraanduiding zich bevindt. De BAG bevat gegevens over zowel bestaande als ingetrokken nummeraanduidingen. Toegestane waarden: 'Naamgeving uitgegeven': Naam is uitgegeven door het bevoegd gezag of geconstateerd. 'Naamgeving ingetrokken': Naam is ingetrokken door het bevoegd gezag. Eindstatussen (het object is beëindigd en de status kan niet meer wijzigen): 'Naamgeving ingetrokken'. |
| geconstateerd | bool | Een aanduiding waarmee kan worden aangegeven dat een nummeraanduiding in de registratie is opgenomen als gevolg van een feitelijke constatering, zonder dat er op het moment van opname sprake was van een regulier brondocument voor deze opname. Het gaat bijvoorbeeld om door burgers aangebrachte nummeraanduidingen die binnen andere processen aan het licht zijn gekomen. In de BAG een indicatie J/N; hier `true` (J) of `false` (N). Basisgegeven, niet authentiek. |
| documentdatum | date32[day] | De datum waarop het brondocument is vastgesteld op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een nummeraanduiding heeft plaatsgevonden. |
| documentnummer | string | De unieke aanduiding van het brondocument op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een nummeraanduiding heeft plaatsgevonden binnen een gemeente. Maximaal 40 tekens. |
| voorkomenidentificatie | int32 | Volgnummer van dit voorkomen (deze versie) van de nummeraanduiding. De identificatie en de voorkomenidentificatie samen bepalen een unieke versie van een object. Het nummer begint bij 1 en wordt bij elke nieuwe versie opgehoogd; nummers van versies die niet in deze gegevens zijn opgenomen (zie beginGeldigheid) ontbreken. |
| beginGeldigheid | date32[day] | De datum waarop deze versie van de nummeraanduiding geldig is in de werkelijkheid conform de ingangsdatum in het brondocument. Als er geen expliciete ingangsdatum van geldigheid is opgenomen, wordt de datum van het brondocument overgenomen. De versies van een object sluiten naadloos op elkaar aan: de eindGeldigheid van een versie is de beginGeldigheid van de volgende. Versies die op dezelfde dag weer zijn vervangen (beginGeldigheid = eindGeldigheid) en inactieve of niet-BAG-voorkomens zijn in deze gegevens niet opgenomen. |
| eindGeldigheid | date32[day] | De datum waarop de periode van geldigheid van deze versie van de nummeraanduiding eindigt, bijvoorbeeld als gevolg van de vaststelling van een nieuw brondocument. Geldig tot (niet tot en met) deze datum. Leeg als de versie nog geldig is. Een object dat niet meer bestaat heeft een versie met een eindstatus (zie status) en zonder eindGeldigheid. |
| tijdstipRegistratie | timestamp[ms] | Het tijdstip waarop deze versie van de nummeraanduiding is geregistreerd in de registratie van de bronhouder (gemeente) en daarmee authentiek is gemaakt. |
| eindRegistratie | timestamp[ms] | Het tijdstip waarop deze versie van de nummeraanduiding is beëindigd in de registratie van de bronhouder. Een versie krijgt een eindRegistratie op het moment dat zij een eindGeldigheid krijgt; het is het tijdstipRegistratie van de volgende versie. Leeg als de versie nog niet is beëindigd. |
| tijdstipRegistratieLV | timestamp[ms] | Het tijdstip waarop deze versie van de nummeraanduiding is opgenomen in de registratie van de landelijke voorziening (LV BAG). De gegevens zijn vanaf dat moment beschikbaar voor afnemers. |
| tijdstipEindRegistratieLV | timestamp[ms] | Het tijdstip waarop de beëindiging van deze versie van de nummeraanduiding is opgenomen in de landelijke voorziening (LV BAG). Leeg als de versie nog niet is beëindigd. |
| voorgaandeVersie | date32[day] | De beginGeldigheid van de voorgaande versie van de nummeraanduiding; leeg bij de eerste versie. |
| volgendeVersie | date32[day] | De beginGeldigheid van de volgende versie van de nummeraanduiding; leeg bij de laatste versie. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./nummeraanduiding.parquet | 2.0 MB | 1220e4b2be35... |

## Quick Start

```python
import pandas as pd

df = pd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet")
print(df.head())
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
