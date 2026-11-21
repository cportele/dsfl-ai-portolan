"""Directory layout of the Portolan catalog.

The 30 BGT collections are grouped in three subcatalogs, following the stored queries of the BGT
API (values/queries/bgt): topografie-in-gebied (the surfaces that cover an area at ground level),
inrichtingselementen-in-gebied (IMGeo plus) and overige-objecten-in-gebied, plus spoor (lines,
part of wegen-in-gebied, not of the area queries).
"""

from pathlib import Path

GROUPS = {
    "bgt": {
        "topografie": {
            "title": "Topografie (vlakken)",
            "description": (
                "De vlakken van de BGT: wegdelen, terreindelen (begroeid en onbegroeid), waterdelen, "
                "panden en de andere objecten op maaiveldniveau. Op maaiveldniveau "
                "(relatieveHoogteligging 0) bedekken de vlakken het gebied zonder gaten en zonder "
                "overlap, zodat de som van de oppervlakten per soort de verdeling van het gebied geeft, "
                "bijvoorbeeld hoeveel groen, verharding, water of bebouwing een buurt heeft."
            ),
            "types": [
                "wegdeel", "ondersteunendwegdeel", "begroeidterreindeel", "onbegroeidterreindeel",
                "waterdeel", "ondersteunendwaterdeel", "pand", "overigbouwwerk", "kunstwerkdeel",
                "overbruggingsdeel", "scheiding",
            ],
        },
        "inrichtingselementen": {
            "title": "Inrichtingselementen",
            "description": (
                "Bakken (afvalbakken, bloembakken), borden (verkeersborden, straatnaamborden), "
                "installaties, kasten, masten, palen (lichtmasten, hectometerpalen, afsluitpalen), "
                "putten, sensoren, straatmeubilair (banken, fietsenrekken, speeltoestellen, abri's), "
                "water- en weginrichtingselementen en vegetatieobjecten (bomen, hagen). De soort staat "
                "in plusType. Dit is optionele IMGeo-informatie: alleen aanwezig waar de bronhouder "
                "(meestal de gemeente) het bijhoudt."
            ),
            "types": [
                "bak", "bord", "installatie", "kast", "mast", "paal", "put", "sensor",
                "straatmeubilair", "waterinrichtingselement", "weginrichtingselement",
                "vegetatieobject",
            ],
        },
        "overig": {
            "title": "Overige objecten",
            "description": (
                "Spoor en de objecten die niet bij de topografie of de inrichtingselementen horen: "
                "functionele gebieden (bgtType 'kering' voor een waterkering, plusType bijvoorbeeld "
                "'recreatie: park', 'recreatie: speeltuin', 'begraafplaats'), gebouwinstallaties "
                "(plusType 'luifel', 'bordes', 'toegangstrap'), tunneldelen, overige scheidingen "
                "(plusType bijvoorbeeld 'muur', 'kademuur', 'geluidsscherm', 'hek'), ongeclassificeerde "
                "objecten en openbareruimtelabels (de straatnamen op de kaart). Functionele gebieden "
                "overlappen de vlakken van de topografie."
            ),
            "types": [
                "spoor", "functioneelgebied", "gebouwinstallatie", "tunneldeel", "overigescheiding",
                "ongeclassificeerdobject", "openbareruimtelabel",
            ],
        },
    },
}


def group_of(api, typ):
    for group, conf in GROUPS.get(api, {}).items():
        if typ in conf["types"]:
            return group
    if api in GROUPS:
        raise ValueError(f"{api}/{typ} is in no group of layout.GROUPS")
    return None


def rel_dir(api, typ):
    """Directory of a collection relative to the catalog root."""
    group = group_of(api, typ)
    return Path(api, group, typ) if group else Path(api, typ)
