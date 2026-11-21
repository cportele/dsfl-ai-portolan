# Postcodegebied (CBS)

Het gebied van een zescijferige postcode (PC6) met statistische gegevens van het CBS over de inwoners, de huishoudens en de woningen op 1 januari 2024. Dezelfde eigenschappen als de collectie [postcode6](https://bag.ldproxy.net/postcode6/collections/postcode6) van de API. Voor agents: [AGENTS.md](AGENTS.md).

![postcode](https://img.shields.io/badge/postcode-blue) ![statistiek](https://img.shields.io/badge/statistiek-blue) ![inwoners](https://img.shields.io/badge/inwoners-blue) ![huishoudens](https://img.shields.io/badge/huishoudens-blue) ![woningen](https://img.shields.io/badge/woningen-blue) ![CBS](https://img.shields.io/badge/CBS-blue)

## Spatial Coverage

- **Bounding Box**: [4.245784013761224, 51.90019436992668, 5.62195318764413, 52.294840957316545]

## Temporal Coverage

- **Start**: 2024-01-01T00:00:00Z
- **End**: ongoing

## Schema

| Column | Type | Description |
|--------|------|-------------|
| postcode | string | De postcode, vier cijfers en twee hoofdletters zonder spatie (bijvoorbeeld 3811LM). De postcode is de id van het object (feature id). |
| aantal_inwoners | int32 | Het aantal inwoners. |
| aantal_mannen | int32 | Het aantal mannen. |
| aantal_vrouwen | int32 | Het aantal vrouwen. |
| aantal_inwoners_0_tot_15_jaar | int32 | Het aantal inwoners jonger dan 15 jaar. |
| aantal_inwoners_15_tot_25_jaar | int32 | Het aantal inwoners van 15 tot 25 jaar. |
| aantal_inwoners_25_tot_45_jaar | int32 | Het aantal inwoners van 25 tot 45 jaar. |
| aantal_inwoners_45_tot_65_jaar | int32 | Het aantal inwoners van 45 tot 65 jaar. |
| aantal_inwoners_65_jaar_en_ouder | int32 | Het aantal inwoners van 65 jaar en ouder. |
| percentage_geb_nederland_herkomst_nederland | int32 | Het percentage inwoners dat in Nederland is geboren en van wie beide ouders in Nederland zijn geboren. |
| percentage_geb_nederland_herkomst_overig_europa | int32 | Het percentage inwoners dat in Nederland is geboren, met een herkomst in Europa buiten Nederland. |
| percentage_geb_nederland_herkomst_buiten_europa | int32 | Het percentage inwoners dat in Nederland is geboren, met een herkomst buiten Europa. |
| percentage_geb_buiten_nederland_herkomst_europa | int32 | Het percentage inwoners dat in Europa buiten Nederland is geboren. |
| percentage_geb_buiten_nederland_herkmst_buiten_europa | int32 | Het percentage inwoners dat buiten Europa is geboren. |
| aantal_part_huishoudens | int32 | Het aantal particuliere huishoudens, zonder institutionele huishoudens (bijvoorbeeld in verzorgingshuizen). |
| aantal_eenpersoonshuishoudens | int32 | Het aantal particuliere huishoudens van één persoon. |
| aantal_meerpersoonshuishoudens_zonder_kind | int32 | Het aantal particuliere huishoudens van meer personen zonder thuiswonende kinderen (paren en overige huishoudens). |
| aantal_eenouderhuishoudens | int32 | Het aantal particuliere huishoudens van één ouder met thuiswonende kinderen. |
| aantal_tweeouderhuishoudens | int32 | Het aantal particuliere huishoudens van twee ouders met ten minste één thuiswonend kind. |
| gemiddelde_huishoudensgrootte | decimal128(3, 1) | Het aantal inwoners in particuliere huishoudens gedeeld door het aantal particuliere huishoudens, op één decimaal afgerond. |
| aantal_woningen | int32 | Het aantal woningen volgens de BAG, verblijfsobjecten met ten minste een woonfunctie. |
| aantal_woningen_bouwjaar_voor_1945 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar voor 1945. |
| aantal_woningen_bouwjaar_45_tot_65 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 1945 tot 1965. |
| aantal_woningen_bouwjaar_65_tot_75 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 1965 tot 1975. |
| aantal_woningen_bouwjaar_75_tot_85 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 1975 tot 1985. |
| aantal_woningen_bouwjaar_85_tot_95 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 1985 tot 1995. |
| aantal_woningen_bouwjaar_95_tot_05 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 1995 tot 2005. |
| aantal_woningen_bouwjaar_05_tot_15 | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 2005 tot 2015. |
| aantal_woningen_bouwjaar_15_en_later | int32 | Het aantal woningen met een oorspronkelijk bouwjaar van 2015 of later. |
| aantal_meergezins_woningen | int32 | Het aantal woningen in een pand met andere woningen of bedrijfsruimten, zoals flats, appartementen en bovenwoningen. |
| percentage_koopwoningen | int32 | Het percentage woningen dat door de (toekomstige) eigenaar wordt bewoond of een tweede woning is. |
| percentage_huurwoningen | int32 | Het percentage woningen dat niet door de eigenaar wordt bewoond; een woning zonder ingeschreven bewoners geldt als huurwoning. |
| aantal_huurwoningen_in_bezit_woningcorporaties | int32 | Het aantal huurwoningen in bezit van woningcorporaties (toegelaten instellingen volkshuisvesting); niet hetzelfde als sociale huurwoningen. |
| aantal_niet_bewoonde_woningen | int32 | Het aantal woningen waar niemand in de Basisregistratie Personen (BRP) staat ingeschreven. |
| aantal_personen_met_uitkering_onder_aowlft | int32 | Het aantal inwoners jonger dan de AOW-leeftijd met een werkloosheids-, bijstands- of arbeidsongeschiktheidsuitkering of een daaraan verwante uitkering; wie meerdere uitkeringen heeft telt één keer. |
| gemeentecode | string | De gemeente waarin het postcodegebied ligt. Geen CBS-gegeven over de postcode, afgeleid uit een punt binnen het gebied. Verwijst naar code in de collectie wijkenbuurten/gemeente. |
| wijkcode | string | De wijk waarin het postcodegebied ligt. Geen CBS-gegeven over de postcode, afgeleid uit een punt binnen het gebied. Verwijst naar code in de collectie wijkenbuurten/wijk. |
| buurtcode | string | De buurt waarin het postcodegebied ligt. Geen CBS-gegeven over de postcode, afgeleid uit een punt binnen het gebied. Verwijst naar code in de collectie wijkenbuurten/buurt. |
| geometrie | binary | De begrenzing van het postcodegebied. De postcodegebieden dekken Nederland zonder gaten, ook land zonder adressen. |
| geometrie_bbox | struct<xmin: float, ymin: float, xmax: float, ymax: float> | Bounding box van geometrie (GeoParquet covering), om bij een ruimtelijke selectie rijgroepen over te slaan. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./postcode6.parquet | 620.6 KB | 1220deb554fc... |
| ./thumbnail.png | 167.8 KB | 1220756a99c9... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/postcode6/postcode6/postcode6.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://www.pdok.nl/introductie/-/article/cbspostcode6](https://www.pdok.nl/introductie/-/article/cbspostcode6)

## Processing Notes

Geladen in PostgreSQL/PostGIS met de scripts van de repository dsfl-ai (https://github.com/cportele/dsfl-ai; scripts/load_postcode6.sh, scripts/postcode6.sql), de database achter de API https://bag.ldproxy.net/postcode6. Per objecttype geëxporteerd met de scripts van https://github.com/cportele/dsfl-ai-portolan: gen_sql.py leidt de queries af uit de feature provider van ldproxy, zodat de kolommen de eigenschappen van de API zijn; export.py schrijft de bestanden met GDAL en sorteert ze met gpio langs een Hilbert-curve (GeoParquet 2.0). Bogen zijn benaderd door lijnstukken met een maximale afwijking van 1 mm. Kolommen met verwijzingen bevatten alleen de identificatie.

## Attribution

© CBS, © ESRI Nederland; Bron: Centraal Bureau voor de Statistiek (CBS), CBS Postcode6 2024

## License

[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.nl)

## Contact

Clemens Portele, interactive instruments GmbH <portele@interactive-instruments.de>

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
