# Basisregistratie Adressen en Gebouwen (BAG)

De gegevens van de API https://bag.ldproxy.net/bag als GeoParquet, een collectie per objecttype; de kolomnamen zijn de namen van de eigenschappen van de API. Begin met de algemene aanwijzingen in de [AGENTS.md van de catalogus](../AGENTS.md).

| Collectie | Geometrie |
|---|---|
| [`woonplaats`](woonplaats/AGENTS.md) (Woonplaats) | geometrie |
| [`openbareruimte`](openbareruimte/AGENTS.md) (Openbare ruimte) | geen |
| [`nummeraanduiding`](nummeraanduiding/AGENTS.md) (Nummeraanduiding) | geen |
| [`pand`](pand/AGENTS.md) (Pand) | geometrie |
| [`verblijfsobject`](verblijfsobject/AGENTS.md) (Verblijfsobject) | geometrie |
| [`ligplaats`](ligplaats/AGENTS.md) (Ligplaats) | geometrie |
| [`standplaats`](standplaats/AGENTS.md) (Standplaats) | geometrie |
| [`kenmerkinonderzoek`](kenmerkinonderzoek/AGENTS.md) (Kenmerk in onderzoek) | geen |

## Versies (BAG)

Elke rij is een voorkomen (versie) van een object, met als sleutel `identificatie` +
`voorkomenidentificatie`. De versies van een object sluiten naadloos op elkaar aan, van
`beginGeldigheid` (inclusief) tot `eindGeldigheid` (exclusief, leeg bij de laatste versie). Versies
die op dezelfde dag weer zijn vervangen en inactieve of niet-BAG-voorkomens zijn niet opgenomen,
net als in de API. De versie die vandaag geldig is, zoals de API die zonder `datetime` levert,
hier geteld per status:

```sql
SELECT status, count(*) AS panden
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet'
WHERE beginGeldigheid <= current_date
  AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
GROUP BY ALL ORDER BY panden DESC
```

Vervang `current_date` door een datum voor de versie die op die datum geldig was. Objecten die
niet meer bestaan (bijvoorbeeld `status = 'Pand gesloopt'` of `'Verblijfsobject ingetrokken'`)
hebben een geldige laatste versie met die eindstatus; filter op `status` om alleen bestaande
objecten te krijgen.

<!-- claim-check: identificatie + voorkomenidentificatie is uniek
SELECT identificatie, voorkomenidentificatie, count(*)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet' GROUP BY ALL HAVING count(*) > 1
-->
<!-- claim-check: identificatie + voorkomenidentificatie is uniek
SELECT identificatie, voorkomenidentificatie, count(*)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet' GROUP BY ALL HAVING count(*) > 1
-->
<!-- claim-check: identificatie + voorkomenidentificatie is uniek
SELECT identificatie, voorkomenidentificatie, count(*)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/nummeraanduiding/nummeraanduiding.parquet' GROUP BY ALL HAVING count(*) > 1
-->
<!-- claim-check: identificatie + voorkomenidentificatie is uniek
SELECT identificatie, voorkomenidentificatie, count(*)
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/openbareruimte/openbareruimte.parquet' GROUP BY ALL HAVING count(*) > 1
-->
<!-- claim-check: de versies sluiten naadloos op elkaar aan en vandaag is hoogstens één versie geldig
SELECT identificatie FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet'
WHERE volgendeVersie IS NOT NULL AND eindGeldigheid IS DISTINCT FROM volgendeVersie
UNION ALL
SELECT identificatie FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet' WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
GROUP BY identificatie HAVING count(*) > 1
-->
<!-- claim-check: de versies sluiten naadloos op elkaar aan en vandaag is hoogstens één versie geldig
SELECT identificatie FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet'
WHERE volgendeVersie IS NOT NULL AND eindGeldigheid IS DISTINCT FROM volgendeVersie
UNION ALL
SELECT identificatie FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet' WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
GROUP BY identificatie HAVING count(*) > 1
-->

## Wat een antwoord verandert (BAG)

- **Status**: de bestanden bevatten alle statussen. Woningen in gebruik zijn verblijfsobjecten met
  `list_contains(gebruiksdoel, 'woonfunctie')` en
  `status IN ('Verblijfsobject in gebruik', 'Verblijfsobject in gebruik (niet ingemeten)', 'Verbouwing verblijfsobject')`. Noem woningen in aanbouw ('Verblijfsobject gevormd') apart als ze ertoe doen.
  Panden: Bouwvergunning verleend, Bouw gestart, Pand in gebruik (niet ingemeten), Pand in gebruik,
  Verbouwing pand, Sloopvergunning verleend, Pand gesloopt, Pand buiten gebruik, Niet gerealiseerd
  pand, Pand ten onrechte opgevoerd.
- **Bouwjaar** (`oorspronkelijkBouwjaar`): 9999 is onbekend. Oude panden hebben vaak een geschat
  rond jaar (1600, 1700, 1800); aantallen per jaar vóór ongeveer 1900 zijn grof. `bouwjaarPand` bij
  een verblijfsobject is het oudste bouwjaar van zijn panden, `statusPand` de status van dat pand.
- **Oppervlakte** van een verblijfsobject is de gebruiksoppervlakte; 999999 is geen werkelijke
  oppervlakte. `grondoppervlakte` van een pand is berekend uit de geometrie; `>= 50` sluit schuren en
  garages uit.
- **Gebruiksdoel** is de vergunde gebruiksfunctie (Bouwbesluit 2012), geen soort voorziening
  (sportfunctie omvat ook kantines). Een verblijfsobject met meer gebruiksdoelen telt in een
  groepering op gebruiksdoel in elke groep mee.
- **Veranderingen**: de toestand op de ene datum min die op de andere. Woningen "gebouwd sinds" een
  jaar (`bouwjaarPand`) zijn niet de woningen die erbij zijn gekomen; in oude stadsdelen ontstaan de
  meeste in bestaande panden. Zie het voorbeeld hieronder.
- **'Pand gesloopt'** beëindigt ook een samenvoeging met een buurpand (dat op dezelfde datum groter
  wordt en de verblijfsobjecten overneemt) en een pand dat nooit is gebouwd. Zeg "als gesloopt
  geregistreerd", splits op grootte en controleer de grotere panden (voorbeeld hieronder).
- **`beginGeldigheid`** is de datum van de registratie, soms jaren na de gebeurtenis.
- **Woonboten en woonwagens** (`ligplaats`, `standplaats`) zijn geen verblijfsobjecten en ontbreken in
  elke telling van woningen; tel ze apart ('Plaats aangewezen').
- **Niet in de BAG**: bewoners (zie `postcode6`), bedrijven, eigenaren, prijzen, energielabels.
- **Gemeente, wijk en buurt** van een object zijn afgeleid uit de geometrie van elke versie; namen
  van wijken en buurten zijn alleen binnen een gemeente uniek.

## Voorbeelden (DuckDB)

Verwijzingen: `verblijfsobject.heeftAlsHoofdadres` → `nummeraanduiding`, `nummeraanduiding.ligtAan` → `openbareruimte`, `openbareruimte.ligtIn` → `woonplaats` (`nummeraanduiding.ligtIn` gaat voor indien aanwezig), `verblijfsobject.maaktDeelUitVan` (lijst) → `pand`. Koppel op `identificatie` en kies de versie van het doelobject die op dezelfde datum geldig was. `nummeraanduiding`, `openbareruimte` en `kenmerkinonderzoek` hebben geen geometrie.

De verblijfsobjecten die vandaag geldig zijn in een pand (`maaktDeelUitVan` is een lijst):

```sql
SELECT identificatie, gebruiksdoel, oppervlakte, status
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet'
WHERE list_contains(maaktDeelUitVan, '0307100000370278') AND beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
```

Verblijfsobjecten in gebruik per gebruiksdoel (een verblijfsobject met meer gebruiksdoelen telt in elke groep mee):

```sql
SELECT g AS gebruiksdoel, count(*) AS aantal
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet', unnest(gebruiksdoel) AS u(g)
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date) AND status IN ('Verblijfsobject in gebruik', 'Verblijfsobject in gebruik (niet ingemeten)', 'Verbouwing verblijfsobject')
GROUP BY ALL ORDER BY aantal DESC
```

Hoeveel woningen er sinds 1 januari 2015 netto bij zijn gekomen, per wijk: de toestand nu min de toestand toen, met dezelfde definitie. Ter vergelijking het aantal woningen in panden met een bouwjaar vanaf 2015; dat mist de woningen die in oudere panden zijn gemaakt (kantoren omgebouwd, woningen gesplitst) en negeert wat verdwenen is:

```sql
WITH w AS (
  FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet'
  WHERE list_contains(gebruiksdoel, 'woonfunctie') AND status IN ('Verblijfsobject in gebruik', 'Verblijfsobject in gebruik (niet ingemeten)', 'Verbouwing verblijfsobject'))
SELECT wijkcode, any_value(wijknaam) AS wijknaam,
       count(*) FILTER (WHERE beginGeldigheid <= DATE '2015-01-01'
         AND (eindGeldigheid IS NULL OR eindGeldigheid > DATE '2015-01-01')) AS woningen_2015,
       count(*) FILTER (WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)) AS woningen_nu,
       woningen_nu - woningen_2015 AS netto_erbij,
       count(*) FILTER (WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date) AND bouwjaarPand >= 2015) AS in_nieuwbouw
FROM w
GROUP BY wijkcode ORDER BY netto_erbij DESC
LIMIT 10
```

Als gesloopt geregistreerde panden van minstens 50 m² sinds 2020, naar wat er gebeurd is. De status van de versie ervoor ('Bouwvergunning verleend': nooit gebouwd) en de verblijfsobjecten van de dag voor de registratie: staan die nu in een ander pand, dan is het pand samengevoegd met een buurpand; zijn ze ingetrokken, dan is het echt gesloopt. Een pand zonder verblijfsobjecten is meestal een bijgebouw:

```sql
WITH s AS (
  SELECT identificatie, beginGeldigheid AS registratie, voorgaandeVersie
  FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet'
  WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date) AND status = 'Pand gesloopt'
    AND beginGeldigheid >= DATE '2020-01-01' AND grondoppervlakte >= 50),
ervoor AS (
  SELECT s.identificatie, p.status
  FROM s JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet' p
    ON p.identificatie = s.identificatie AND p.beginGeldigheid = s.voorgaandeVersie),
vbo AS (
  SELECT s.identificatie,
         count(*) FILTER (WHERE nu.status = 'Verblijfsobject ingetrokken') AS ingetrokken,
         count(*) FILTER (WHERE NOT list_contains(nu.maaktDeelUitVan, s.identificatie)
           AND nu.status NOT IN ('Verblijfsobject ingetrokken',
                                 'Niet gerealiseerd verblijfsobject')) AS elders
  FROM s
  JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet' toen
    ON list_contains(toen.maaktDeelUitVan, s.identificatie)
   AND toen.beginGeldigheid <= s.registratie - 1
   AND (toen.eindGeldigheid IS NULL OR toen.eindGeldigheid > s.registratie - 1)
  JOIN 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/verblijfsobject/verblijfsobject.parquet' nu
    ON nu.identificatie = toen.identificatie AND nu.beginGeldigheid <= current_date AND (nu.eindGeldigheid IS NULL OR nu.eindGeldigheid > current_date)
  GROUP BY s.identificatie)
SELECT CASE
         WHEN ervoor.status = 'Bouwvergunning verleend' THEN 'nooit gebouwd'
         WHEN vbo.elders > 0 THEN 'samengevoegd'
         WHEN vbo.ingetrokken > 0 THEN 'gesloopt'
         ELSE 'zonder verblijfsobjecten'
       END AS soort,
       count(*) AS panden
FROM s LEFT JOIN ervoor USING (identificatie) LEFT JOIN vbo USING (identificatie)
GROUP BY ALL ORDER BY panden DESC
```

Alle versies van een pand, de oudste eerst:

```sql
SELECT voorkomenidentificatie, beginGeldigheid, eindGeldigheid, status, oorspronkelijkBouwjaar
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/pand/pand.parquet'
WHERE identificatie = '0307100000370278'
ORDER BY voorkomenidentificatie
```

De gemeenten van een woonplaats (`gemeenteWoonplaatsRelatie` is JSON-tekst):

```sql
SELECT naam, r ->> 'gemeentecode' AS gemeente, r ->> 'beginGeldigheid' AS sinds
FROM 'https://dsfl-ai-417829795942-eu-central-1-an.s3.eu-central-1.amazonaws.com/bag/woonplaats/woonplaats.parquet',
     unnest(CAST(json(gemeenteWoonplaatsRelatie) AS JSON[])) AS u(r)
WHERE beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)
```
