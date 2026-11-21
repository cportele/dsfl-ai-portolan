"""Directory layout of the Portolan catalog.

The 30 BGT collections are grouped in three subcatalogs, following the stored queries of the BGT
API (values/queries/bgt): topografie-in-gebied (the surfaces that cover an area at ground level),
inrichtingselementen-in-gebied (IMGeo plus) and overige-objecten-in-gebied, plus spoor (lines,
part of wegen-in-gebied, not of the area queries).
"""

import re
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
                "Bakken ({bak:plusType}), borden ({bord:plusType}), installaties "
                "({installatie:plusType}), kasten ({kast:plusType}), masten ({mast:plusType}), palen "
                "({paal:plusType}), putten ({put:plusType}), sensoren ({sensor:plusType}), "
                "straatmeubilair ({straatmeubilair:plusType}), waterinrichtingselementen "
                "({waterinrichtingselement:plusType}), weginrichtingselementen "
                "({weginrichtingselement:plusType}) en vegetatieobjecten ({vegetatieobject:plusType}). "
                "De soort staat in plusType; tussen haakjes de meest voorkomende soorten in deze "
                "gegevens. Dit is optionele IMGeo-informatie: alleen aanwezig waar de bronhouder het "
                "bijhoudt."
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
                "Spoor ({spoor:bgtFunctie}) en de objecten die niet bij de topografie of de "
                "inrichtingselementen horen: functionele gebieden ({functioneelgebied:plusType}), "
                "gebouwinstallaties ({gebouwinstallatie:plusType}), tunneldelen, overige scheidingen "
                "({overigescheiding:plusType}), ongeclassificeerde objecten en openbareruimtelabels "
                "(de straatnamen op de kaart). Tussen haakjes de soorten in deze gegevens. "
                "Functionele gebieden overlappen de vlakken van de topografie."
            ),
            "types": [
                "spoor", "functioneelgebied", "gebouwinstallatie", "tunneldeel", "overigescheiding",
                "ongeclassificeerdobject", "openbareruimtelabel",
            ],
        },
    },
}


# "{type:column}" in a group description: the most frequent values of the column in that collection
VALUES = re.compile(r"\{(\w+):(\w+)\}")


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
