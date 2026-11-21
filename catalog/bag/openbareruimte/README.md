# Openbare ruimte (BAG)

Een openbare ruimte is een door het bevoegde gemeentelijke orgaan als zodanig aangewezen en van een naam voorziene buitenruimte die binnen één woonplaats is gelegen. Meestal een straat; ook water, spoorbanen, terreinen, kunstwerken, landschappelijke en administratieve gebieden. De BAG bevat geen geometrie van openbare ruimten. Met historie: een rij per voorkomen (versie) van een object, sleutel identificatie en voorkomenidentificatie. Dezelfde eigenschappen als de collectie [openbareruimte](https://bag.ldproxy.net/bag/collections/openbareruimte) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![BAG](https://img.shields.io/badge/BAG-blue) ![adressen](https://img.shields.io/badge/adressen-blue) ![gebouwen](https://img.shields.io/badge/gebouwen-blue) ![panden](https://img.shields.io/badge/panden-blue) ![verblijfsobjecten](https://img.shields.io/badge/verblijfsobjecten-blue) ![nummeraanduidingen](https://img.shields.io/badge/nummeraanduidingen-blue) ![openbare ruimten](https://img.shields.io/badge/openbare_ruimten-blue) ![woonplaatsen](https://img.shields.io/badge/woonplaatsen-blue)

## Spatial Coverage

- **Bounding Box**: [5.306458635645041, 52.10838438725852, 5.484329664176055, 52.21915384787237]

## Temporal Coverage

- **Start**: 1994-05-09T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| identificatie | string | De unieke aanduiding van een openbare ruimte. De identificatie bestaat uit 16 cijfers: de viercijferige gemeentecode van de gemeente die de identificatie heeft toegekend, de tweecijferige objecttypecode en een tiencijferig objectvolgnummer. De gemeentecode in de identificatie zegt niets over de gemeente waarin het object nu ligt. De identificatie verandert niet zolang het object bestaat; alle voorkomens (versies) van een object hebben dezelfde identificatie. |
| naam | string | De naam die aan een openbare ruimte is toegekend in een daartoe strekkend formeel gemeentelijk besluit, meestal een straatnaam. Maximaal 80 tekens. Dezelfde naam kan in meerdere woonplaatsen voorkomen; een openbare ruimte die door twee woonplaatsen loopt is als twee openbare ruimten geregistreerd. |
| verkorteNaam | string | Een verkorte naam van de openbare ruimte als de naam langer is dan 24 tekens, afgekort door het Kadaster volgens NEN 5825. Geen onderdeel van de BAG en geen authentiek gegeven; alleen de volledige naam is officieel. Maximaal 24 tekens. |
| type | string | De aard van de als zodanig benoemde openbare ruimte. Toegestane waarden: 'Weg': Gebaand gedeelte voor het wegverkeer en vliegverkeer te land, bijvoorbeeld een straat. 'Water': Grondoppervlak in principe bedekt met water, bijvoorbeeld een rivier. 'Spoorbaan': Gebaand gedeelte voor het verkeer over rails. 'Terrein': Door een fysiek voorkomen gekarakteriseerd zichtbaar begrensd stuk grond, bijvoorbeeld een parkeerterrein. 'Kunstwerk': Civiel-technisch werk voor de infrastructuur van wegen, water, spoorbanen, waterkeringen en/of leidingen, bijvoorbeeld een brug. 'Landschappelijk gebied': Geografisch benoemd gebied (bijvoorbeeld Veluwe) of functioneel gebied (bijvoorbeeld bedrijventerrein, bungalowpark, jachthaven). 'Administratief gebied': Op basis van wet- en regelgeving afgebakend gebied, bijvoorbeeld een stadsdeel. |
| ligtIn | string | De unieke aanduiding van de woonplaats waarbinnen de openbare ruimte is gelegen. Een openbare ruimte ligt in precies één woonplaats. Als een nummeraanduiding zelf een woonplaats heeft (nummeraanduiding.ligtIn), dan gaat die voor. Verwijst naar identificatie in de collectie bag/woonplaats. |
| status | string | De fase van de levenscyclus van een openbare ruimte waarin de betreffende openbare ruimte zich bevindt. De BAG bevat gegevens over zowel bestaande als ingetrokken openbare ruimten. Toegestane waarden: 'Naamgeving uitgegeven': Naam is uitgegeven door het bevoegd gezag of geconstateerd. 'Naamgeving ingetrokken': Naam is ingetrokken door het bevoegd gezag. Eindstatussen (het object is beëindigd en de status kan niet meer wijzigen): 'Naamgeving ingetrokken'. |
| geconstateerd | bool | Een aanduiding waarmee kan worden aangegeven dat een openbare ruimte in de registratie is opgenomen als gevolg van een feitelijke constatering, zonder dat er op het moment van opname sprake was van een regulier brondocument voor deze opname. Het gaat bijvoorbeeld om door burgers aangebrachte benamingen die binnen andere processen aan het licht zijn gekomen. In de BAG een indicatie J/N; hier `true` (J) of `false` (N). Basisgegeven, niet authentiek. |
| documentdatum | date32[day] | De datum waarop het brondocument is vastgesteld op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een openbare ruimte heeft plaatsgevonden. |
| documentnummer | string | De unieke aanduiding van het brondocument op basis waarvan een opname, mutatie of een verwijdering van gegevens ten aanzien van een openbare ruimte heeft plaatsgevonden binnen een gemeente. Maximaal 40 tekens. |
| voorkomenidentificatie | int32 | Volgnummer van dit voorkomen (deze versie) van de openbare ruimte. De identificatie en de voorkomenidentificatie samen bepalen een unieke versie van een object. Het nummer begint bij 1 en wordt bij elke nieuwe versie opgehoogd; nummers van versies die niet in deze gegevens zijn opgenomen (zie beginGeldigheid) ontbreken. |
| beginGeldigheid | date32[day] | De datum waarop deze versie van de openbare ruimte geldig is in de werkelijkheid conform de ingangsdatum in het brondocument. Als er geen expliciete ingangsdatum van geldigheid is opgenomen, wordt de datum van het brondocument overgenomen. De versies van een object sluiten naadloos op elkaar aan: de eindGeldigheid van een versie is de beginGeldigheid van de volgende. Versies die op dezelfde dag weer zijn vervangen (beginGeldigheid = eindGeldigheid) en inactieve of niet-BAG-voorkomens zijn in deze gegevens niet opgenomen. |
| eindGeldigheid | date32[day] | De datum waarop de periode van geldigheid van deze versie van de openbare ruimte eindigt, bijvoorbeeld als gevolg van de vaststelling van een nieuw brondocument. Geldig tot (niet tot en met) deze datum. Leeg als de versie nog geldig is. Een object dat niet meer bestaat heeft een versie met een eindstatus (zie status) en zonder eindGeldigheid. |
| tijdstipRegistratie | timestamp[ms] | Het tijdstip waarop deze versie van de openbare ruimte is geregistreerd in de registratie van de bronhouder (gemeente) en daarmee authentiek is gemaakt. |
| eindRegistratie | timestamp[ms] | Het tijdstip waarop deze versie van de openbare ruimte is beëindigd in de registratie van de bronhouder. Een versie krijgt een eindRegistratie op het moment dat zij een eindGeldigheid krijgt; het is het tijdstipRegistratie van de volgende versie. Leeg als de versie nog niet is beëindigd. |
| tijdstipRegistratieLV | timestamp[ms] | Het tijdstip waarop deze versie van de openbare ruimte is opgenomen in de registratie van de landelijke voorziening (LV BAG). De gegevens zijn vanaf dat moment beschikbaar voor afnemers. |
| tijdstipEindRegistratieLV | timestamp[ms] | Het tijdstip waarop de beëindiging van deze versie van de openbare ruimte is opgenomen in de landelijke voorziening (LV BAG). Leeg als de versie nog niet is beëindigd. |
| voorgaandeVersie | date32[day] | De beginGeldigheid van de voorgaande versie van de openbare ruimte; leeg bij de eerste versie. |
| volgendeVersie | date32[day] | De beginGeldigheid van de volgende versie van de openbare ruimte; leeg bij de laatste versie. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./openbareruimte.parquet | 41.6 KB | 12201b3ef81f... |

## Quick Start

```python
import pandas as pd

df = pd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/openbareruimte/openbareruimte.parquet")
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
