# Kenmerk in onderzoek (BAG)

Een kenmerk (attribuut of relatie) van een BAG-object waarvoor wordt of werd onderzocht of het gegeven juist is. Als een gegeven in onderzoek is, mogen gebruikers een ander gegeven gebruiken; de bronhouder moet het onderzoek binnen zes maanden afronden. Elk record heeft een eigen geldigheidsperiode, los van de versies van het object. Het plaatsen in onderzoek levert een record met inOnderzoek = true; het afronden beëindigt dat record en levert een nieuw record met inOnderzoek = false. Kenmerken per objecttype: woonplaats: naam, geometrie, status; openbareruimte: naam, type, status, ligt in; nummeraanduiding: huisnummer, huisletter, huisnummertoevoeging, postcode, type adresseerbaar object, status, ligt in, ligt aan; pand: geometrie, oorspronkelijk bouwjaar, status; verblijfsobject: geometrie, gebruiksdoel, oppervlakte, status, maakt deel uit van, heeft als hoofdadres, heeft als nevenadres; standplaats: geometrie, status, heeft als hoofdadres, heeft als nevenadres; ligplaats: geometrie, status, heeft als hoofdadres, heeft als nevenadres. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [kenmerkinonderzoek](https://bag.ldproxy.net/bag/collections/kenmerkinonderzoek) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.306458635645041, 52.10838438725852, 5.484329664176055, 52.21915384787237]

## Temporal Coverage

- **Start**: 2010-10-05T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| id | int64 | Technische sleutel van het record; geen BAG-gegeven. |
| objecttype | string | Het type van het BAG-object dat in onderzoek is geplaatst: 'WPL' (woonplaats), 'OPR' (openbareruimte), 'NUM' (nummeraanduiding), 'PND' (pand), 'VBO' (verblijfsobject), 'STA' (standplaats), 'LIG' (ligplaats). |
| object | string | Het BAG-object waarvan een kenmerk in onderzoek is geplaatst. |
| kenmerk | string | De naam van het attribuut of de relatie van het object dat in onderzoek is geplaatst, zoals in de BAG benoemd (met spaties, bijvoorbeeld 'oorspronkelijk bouwjaar' voor oorspronkelijkBouwjaar). |
| inOnderzoek | bool | Geeft aan of het kenmerk in deze periode in onderzoek is (`true`, in de BAG J) of niet (`false`, N). |
| documentdatum | date32[day] | De datum van het document waarin de grondslag van het onderzoek wordt vastgelegd. |
| documentnummer | string | Het nummer van het document waarin de grondslag van het onderzoek wordt vastgelegd. Maximaal 40 tekens. |
| beginGeldigheid | date32[day] | De datum waarop deze toestand ingaat: bij inOnderzoek = true de datum waarop het kenmerk bij de bronhouder in onderzoek is geplaatst. |
| eindGeldigheid | date32[day] | De datum waarop deze toestand eindigt (niet tot en met): bij inOnderzoek = true de datum waarop het onderzoek is afgerond. Leeg als de toestand nog geldt. |
| tijdstipRegistratie | timestamp[ms] | Het tijdstip waarop het record is geregistreerd bij de bronhouder. |
| eindRegistratie | timestamp[ms] | Het tijdstip waarop de registratie van het record is beëindigd bij de bronhouder. |
| tijdstipRegistratieLV | timestamp[ms] | Het tijdstip waarop het record is geregistreerd in de landelijke voorziening. |
| tijdstipEindRegistratieLV | timestamp[ms] | Het tijdstip waarop de beëindiging van het record is opgenomen in de landelijke voorziening. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./kenmerkinonderzoek.parquet | 41.5 KB | 12205e419943... |

## Quick Start

```python
import pandas as pd

df = pd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/kenmerkinonderzoek/kenmerkinonderzoek.parquet")
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
