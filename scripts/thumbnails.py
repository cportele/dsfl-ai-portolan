#!/usr/bin/env python3
"""Render a thumbnail.png for every geospatial collection of the catalog.

`portolan add` adopts an image named thumbnail.png in the collection directory as the collection's
thumbnail asset (PTL-VIZ-001), so this runs before build_catalog.py.

What a thumbnail shows:
- the versions that are current now (the rule of the APIs without `datetime`); a collection
  without current versions shows all versions;
- coloured by the attribute that classifies the objects (STYLE), categories ranked by frequency,
  the rest grey; a few collections use a sequential scale instead;
- large fabrics (more than DENSE features) in a 2.4 x 1.6 km window around their densest area,
  so single objects stay visible; everything else at its full extent with the boundary of the
  gemeente for orientation;
- 3:2, 600 x 400 px, no basemap (the data only), so the build stays offline and reproducible.

Run with the Python of the portolan-cli tool environment (duckdb, geopandas, matplotlib):

  <portolan-cli python> -I thumbnails.py <manifest.json> <catalog dir>
"""

import json
import sys
from pathlib import Path

import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import shapely  # noqa: E402
from geopandas import GeoSeries  # noqa: E402
from matplotlib.colors import Normalize, to_hex  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))  # run with python -I
from layout import rel_dir  # noqa: E402

CURRENT = {
    "bag": "beginGeldigheid <= current_date AND (eindGeldigheid IS NULL OR eindGeldigheid > current_date)",
    "bgt": "eindRegistratie IS NULL",
}

# (column, kind): the attribute that colours a collection; default: the first BGT_CLASS column.
STYLE = {
    ("bag", "pand"): ("oorspronkelijkBouwjaar", "seq"),
    ("bag", "verblijfsobject"): ("gebruiksdoel", "cat"),
    ("bag", "woonplaats"): ("naam", "cat"),
    ("bag", "ligplaats"): ("status", "cat"),
    ("bag", "standplaats"): ("status", "cat"),
    ("bgt", "pand"): ("bronhouder", "cat"),
    ("bgt", "openbareruimtelabel"): ("bronhouder", "cat"),
    ("bgt", "tunneldeel"): ("bronhouder", "cat"),
    ("bgt", "ongeclassificeerdobject"): ("bronhouder", "cat"),
    ("wijkenbuurten", "gemeente"): ("naam", "cat"),
    ("wijkenbuurten", "wijk"): ("code", "cat"),
    ("wijkenbuurten", "buurt"): ("wijk", "cat"),
    ("postcode6", "postcode6"): ("aantal_inwoners", "seq"),
}
BGT_CLASS = ["bgtFunctie", "bgtFysiekVoorkomen", "bgtType", "plusType", "plusFunctie"]

# Categorical palette (colour-blind safe, distinct at small size); index 0 is the most frequent.
PALETTE = ["#1f6fb4", "#e0812a", "#2e9e5b", "#c8413b", "#8a62b8", "#8c5a3c", "#d266a8",
           "#6b8e23", "#17a2b8", "#b8a21a"]
OTHER = "#b9b9b4"
SEQ = {("bag", "pand"): "viridis", ("postcode6", "postcode6"): "magma_r"}
BACKGROUND = "#f6f5f1"
BOUNDARY = "#77756d"
W, H, DPI = 6.0, 4.0, 100
DENSE = 5000
WINDOW = (2400.0, 1600.0)


def frame(xmin, ymin, xmax, ymax, minimum=600.0):
    """Expand a bbox to 3:2 with a margin."""
    w, h = max(xmax - xmin, minimum), max(ymax - ymin, minimum / 1.5)
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    w, h = w * 1.06, h * 1.06
    if w / h < 1.5:
        w = h * 1.5
    else:
        h = w / 1.5
    return cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2


def render(db, catalog, t, gemeente):
    api, typ = t["api"], t["type"]
    geom = next(g["name"] for g in t["geometries"] if g["primary"])
    path = catalog / rel_dir(api, typ) / f"{typ}.parquet"
    names = {c["name"] for c in t["columns"]}
    where = CURRENT.get(api, "true")
    if not db.sql(f"SELECT count(*) FROM '{path}' WHERE {where}").fetchone()[0]:
        where = "true"
    col, kind = STYLE.get((api, typ), (next((c for c in BGT_CLASS if c in names), None), "cat"))
    value = "NULL"
    if col:
        value = f"{col}[1]" if any(c["name"] == col and c["type"].startswith("array") for c in t["columns"]) else col
    rows = db.sql(
        f"SELECT ST_AsWKB({geom}) AS g, {value} AS v FROM '{path}' WHERE {where} AND {geom} IS NOT NULL"
    ).fetchall()
    geoms = GeoSeries(shapely.from_wkb([bytes(r[0]) for r in rows]))
    values = [r[1] for r in rows]
    b = geoms.bounds
    polygons = geoms.geom_type.str.endswith("Polygon")
    if len(geoms) > DENSE and polygons.mean() > 0.9:
        # a fabric of polygons: a window around the densest 200 m cell of the bbox centres
        cx, cy = (b.minx + b.maxx) / 2, (b.miny + b.maxy) / 2
        cells = ((cx // 200).astype(int).astype(str) + "/" + (cy // 200).astype(int).astype(str)).value_counts()
        gx, gy = (int(v) for v in cells.index[0].split("/"))
        mx, my = gx * 200 + 100, gy * 200 + 100
        box = (mx - WINDOW[0] / 2, my - WINDOW[1] / 2, mx + WINDOW[0] / 2, my + WINDOW[1] / 2)
        context = False
    else:
        # full extent without outliers (1st to 99th percentile of the bbox centres)
        cx, cy = (b.minx + b.maxx) / 2, (b.miny + b.maxy) / 2
        q = (0.01, 0.99) if len(geoms) >= 100 else (0.0, 1.0)
        box = frame(*cx.quantile(q[0:1]), *cy.quantile(q[0:1]), *cx.quantile(q[1:2]), *cy.quantile(q[1:2]))
        if len(geoms) < 100:
            box = frame(b.minx.min(), b.miny.min(), b.maxx.max(), b.maxy.max())
        context = True
    scale = (box[2] - box[0]) / (W * DPI)  # metres per pixel

    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_facecolor(BACKGROUND)
    fig.patch.set_facecolor(BACKGROUND)
    if context and gemeente is not None and typ != "gemeente":
        gemeente.boundary.plot(ax=ax, color=BOUNDARY, linewidth=0.6, zorder=1)

    if kind == "seq" and col:
        known = [v for v in values if v is not None and v < 9999]
        lo, hi = (min(known), max(known)) if known else (0, 1)
        if (api, typ) == ("bag", "pand"):
            lo, hi = max(lo, 1850), min(hi, 2025)
        norm, cmap = Normalize(lo, hi, clip=True), plt.get_cmap(SEQ[(api, typ)])
        colors = [to_hex(cmap(norm(v))) if v is not None and v < 9999 else OTHER for v in values]
    else:
        ranked = {}
        for v in values:
            if v is not None and v not in ("waardeOnbekend", "geenWaarde"):
                ranked[v] = ranked.get(v, 0) + 1
        top = [v for v, _ in sorted(ranked.items(), key=lambda x: -x[1])]
        if api != "wijkenbuurten":  # areas: every category gets a colour, cycling the palette
            top = top[: len(PALETTE)]
        offset = sum(map(ord, typ)) % len(PALETTE) if len(top) <= 1 else 0  # siblings differ
        colors = [PALETTE[(top.index(v) + offset) % len(PALETTE)] if v in top else OTHER for v in values]
        if not top:  # no classifying attribute or no values: one colour, different per collection
            colors = [PALETTE[sum(map(ord, typ)) % len(PALETTE)]] * len(values)

    # objects smaller than a few pixels are drawn as markers, otherwise they vanish at this scale
    size = (b.maxx - b.minx).combine(b.maxy - b.miny, max)
    small = (size < 4 * scale).to_numpy()
    kinds = geoms.geom_type.str.replace("Multi", "").to_numpy()
    kinds[small] = "Point"
    geoms = GeoSeries([g.representative_point() if s else g for g, s in zip(geoms, small)])
    n_points = int((kinds == "Point").sum())
    for k in ("Polygon", "LineString", "Point"):
        sel = kinds == k
        if not sel.any():
            continue
        sub, cols = geoms[sel], [c for c, s in zip(colors, sel) if s]
        if k == "Polygon":
            edge = "#ffffff" if not context else cols
            sub.plot(ax=ax, color=cols, edgecolor=edge, linewidth=0.15 if not context else 0.5, zorder=2)
        elif k == "LineString":
            sub.plot(ax=ax, color=cols, linewidth=0.9 if not context else 1.6, zorder=3)
        else:
            ms = 60 if n_points < 50 else 24 if n_points < 500 else 10 if n_points < 5000 else 3
            sub.plot(ax=ax, color=cols, markersize=ms, edgecolor="#ffffff", linewidth=0.4, zorder=4)
    ax.set_xlim(box[0], box[2])
    ax.set_ylim(box[1], box[3])
    ax.set_aspect("equal")
    ax.set_axis_off()
    out = path.parent / "thumbnail.png"
    fig.savefig(out, dpi=DPI, facecolor=BACKGROUND)
    plt.close(fig)
    return out, len(geoms), "window" if not context else "extent"


def main(manifest, catalog):
    catalog = Path(catalog)
    types = json.loads(Path(manifest).read_text())
    db = duckdb.connect()
    db.sql("LOAD spatial")
    gemeente = None
    g = catalog / rel_dir("wijkenbuurten", "gemeente") / "gemeente.parquet"
    if g.exists():
        gemeente = GeoSeries(shapely.from_wkb([bytes(r[0]) for r in db.sql(
            f"SELECT ST_AsWKB(geometrie) FROM '{g}'").fetchall()]))
    for t in types:
        if not t["geometries"]:
            continue
        out, count, how = render(db, catalog, t, gemeente)
        print(f"{out.relative_to(catalog)}: {count} features, {how}", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
