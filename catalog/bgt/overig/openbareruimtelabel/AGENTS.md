# OpenbareRuimteLabel (bgt/overig/openbareruimtelabel)

De collectie `openbareruimtelabel` van de API https://bag.ldproxy.net/bgt als één bestand, `openbareruimtelabel.parquet` (aantal rijen: `table:row_count` in `collection.json`). Algemene aanwijzingen: [AGENTS.md van de catalogus](../../../AGENTS.md); versies en verwijzingen van de registratie: [AGENTS.md van bgt](../../AGENTS.md). Beschrijvingen van de kolommen: `collection.json` (`table:columns`) en de README.

- Geometriekolommen: `geometrie` (primair); CRS EPSG:28992, bounding-boxkolommen `<naam>_bbox`.
- Actuele versies: `WHERE eindRegistratie IS NULL`.
- Lijsten: `hoek`.
- Verwijzingen: `identificatieBAGOPR` → `bag/openbareruimte.identificatie`.

## Voorbeelden (DuckDB)

Vijf actuele versies:

```sql
SELECT * EXCLUDE (geometrie)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/overig/openbareruimtelabel/openbareruimtelabel.parquet'
WHERE eindRegistratie IS NULL
LIMIT 5
```

De verwijzing `identificatieBAGOPR` volgen:

```sql
SELECT t.identificatie, r.*
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bgt/overig/openbareruimtelabel/openbareruimtelabel.parquet' t
JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/openbareruimte/openbareruimte.parquet' r ON r.identificatie = t.identificatieBAGOPR AND r.beginGeldigheid <= current_date AND (r.eindGeldigheid IS NULL OR r.eindGeldigheid > current_date)
WHERE t.eindRegistratie IS NULL
LIMIT 5
```

## Waarden en definities

Naam en plaatsingspunten van een in de BAG geregistreerde OPENBARE RUIMTE. English: street name label: name and label positions of a public space (street) of the BAG.

De waarden van de classificerende eigenschappen, met hun definitie. Bron: de Gegevenscatalogus BGT 1.2,
de Gegevenscatalogus IMGeo 2.2 en de IMGeo-waardelijsten van 1 juli 2020, aangevuld met de waarden die
in de gegevens voorkomen (stand 30 oktober 2026).

### bgtStatus (waardelijst Status; BGT, authentiek)

- `bestaand`: Situatie waarin het object wordt / kan worden gebruikt voor het doel waarvoor het is gebouwd / aangelegd.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### plusStatus (waardelijst StatusPlus; IMGeo-plus, niet authentiek; alleen gevuld als de bronhouder het bijhoudt)

- `plan`: Situatie die ontstaat op het moment van verlening van een beschikking voor bouw of aanleg en duurt tot het moment waarop het object gereed is voor het beoogde gebruik.
- `historie`: Situatie waarin het geregistreerde object fysiek niet meer bestaat.

Daarnaast als reden voor het ontbreken van een waarde: `geenWaarde`.

### openbareRuimteType (waardelijst TypeOpenbareRuimte; BGT, authentiek in een andere basisregistratie)

- `Weg`: Gebaand gedeelte voor het wegverkeer en vliegverkeer te land.
- `Water`: Grondoppervlak in principe bedekt met water.
- `Spoorbaan`: Gebaand gedeelte voor het verkeer over rails.
- `Terrein`: Door een fysiek voorkomen gekarakteriseerd zichtbaar begrensd stuk grond.
- `Kunstwerk`: Civiel-technisch werk voor de infrastructuur van wegen, water, spoorbanen, waterkeringen en/of leidingen en niet bedoeld voor permanent menselijk verblijf.
- `Landschappelijk gebied`: Definitie ontbreekt in de BAG.
- `Administratief gebied`: Een niet tastbaar begrensd grondoppervlak dat als eenheid geldt voor bestuurlijke verantwoordelijkheid, voor bedrijfsvoering, waarbinnen een specifieke rechtsverhouding te onderscheiden is of waarvoor een specifieke functie of bestemming geldt.
