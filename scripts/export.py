#!/usr/bin/env python3
"""Write one GeoParquet file per feature type of the manifest (gen_sql.py).

GeoParquet 2.0: WKB with the Parquet GEOMETRY logical type (CRS EPSG:28992 as PROJJSON, as in the
database), geospatial row group statistics and a bbox covering column per geometry column, zstd.
Two steps:

1. GDAL writes the query result. ogr2ogr drops all geometry columns but the first when writing
   Parquet; this script creates the geometry fields before the first feature, which the driver
   supports.
2. gpio (geoparquet-io, part of the portolan-cli installation) sorts the rows along a Hilbert curve
   of the primary geometry and writes GeoParquet 2.0 with row groups of 49,152 rows (whole
   2,048-row vectors), so a spatial filter can skip row groups. PostGIS ORDER BY geometry does not
   give that locality; GDAL's USE_PARQUET_GEO_TYPES had no effect with the local GDAL build.

Tables without geometry (nummeraanduiding, openbareruimte, kenmerkinonderzoek) are plain Parquet,
sorted by identificatie and version.

Usage: export.py <manifest.json> <catalog dir> [<api>[/<type>] ...]
Database: environment PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD (defaults: the docker-compose
database on 127.0.0.1:5436, database/user/password bag). gpio: environment GPIO, else gpio on the
PATH, else the one in the uv tool environment of portolan-cli.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from osgeo import ogr, osr

from layout import rel_dir

ogr.UseExceptions()

ROW_GROUP_SIZE = 49152


def connection():
    env = os.environ
    return "PG:" + " ".join(
        [
            f"host={env.get('PGHOST', '127.0.0.1')}",
            f"port={env.get('PGPORT', '5436')}",
            f"dbname={env.get('PGDATABASE', 'bag')}",
            f"user={env.get('PGUSER', 'bag')}",
            f"password={env.get('PGPASSWORD', 'bag')}",
        ]
    )


def gpio():
    path = (
        os.environ.get("GPIO")
        or shutil.which("gpio")
        or str(Path.home() / ".local/share/uv/tools/portolan-cli/bin/gpio")
    )
    if not Path(path).exists():
        sys.exit("gpio not found, set GPIO")
    return path


def order_by(t):
    names = [c["name"] for c in t["columns"]]
    keys = [
        f'x."{k}"'
        for k in ("identificatie", "id", "postcode", "voorkomenidentificatie", "tijdstipRegistratie")
        if k in names
    ]
    return " ORDER BY " + ", ".join(keys) if keys else ""


def write(src, t, target):
    """GDAL step; returns row count and geometry types per geometry column."""
    lyr = src.ExecuteSQL(f"SELECT * FROM ({t['sql']}) x{order_by(t)}")
    try:
        defn = lyr.GetLayerDefn()
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(28992)
        target.unlink(missing_ok=True)
        ds = ogr.GetDriverByName("Parquet").CreateDataSource(str(target))
        options = [
            "COMPRESSION=ZSTD",
            f"ROW_GROUP_SIZE={ROW_GROUP_SIZE}",
            "CREATOR=dsfl-ai scripts/portolan/export.py",
        ]
        if defn.GetGeomFieldCount():
            options += ["WRITE_COVERING_BBOX=YES", "EDGES=PLANAR"]
        out = ds.CreateLayer(target.stem, geom_type=ogr.wkbNone, options=options)
        geom_types = {}
        for i in range(defn.GetGeomFieldCount()):
            gf = ogr.GeomFieldDefn(defn.GetGeomFieldDefn(i).GetName(), ogr.wkbUnknown)
            gf.SetSpatialRef(srs)
            out.CreateGeomField(gf)
            geom_types[gf.GetName()] = set()
        for i in range(defn.GetFieldCount()):
            out.CreateField(defn.GetFieldDefn(i))
        odefn = out.GetLayerDefn()
        n = 0
        for f in lyr:
            o = ogr.Feature(odefn)
            o.SetFrom(f)
            for i in range(odefn.GetGeomFieldCount()):
                g = o.GetGeomFieldRef(i)
                if g is not None:
                    geom_types[odefn.GetGeomFieldDefn(i).GetName()].add(g.GetGeometryName())
            out.CreateFeature(o)
            n += 1
        ds = None
        return n, {k: sorted(v) for k, v in geom_types.items()}
    finally:
        src.ReleaseResultSet(lyr)


def hilbert(tmp, target, geometry):
    subprocess.run(
        [gpio(), "sort", "hilbert", "-g", geometry, "--row-group-size", str(ROW_GROUP_SIZE),
         "--geoparquet-version", "2.0", str(tmp), str(target)],
        check=True,
        capture_output=True,
    )
    tmp.unlink()


def main(manifest, catalog, *only):
    types = json.loads(Path(manifest).read_text())
    src = ogr.Open(connection())
    for t in types:
        key = f"{t['api']}/{t['type']}"
        if only and not any(key == o or t["api"] == o for o in only):
            continue
        cdir = Path(catalog) / rel_dir(t["api"], t["type"])
        cdir.mkdir(parents=True, exist_ok=True)
        target = cdir / f"{t['type']}.parquet"
        start = time.time()
        primary = [g["name"] for g in t["geometries"] if g["primary"]]
        if primary:
            tmp = cdir / f".{t['type']}.unsorted.parquet"
            n, geom_types = write(src, t, tmp)
            target.unlink(missing_ok=True)
            hilbert(tmp, target, primary[0])
        else:
            n, geom_types = write(src, t, target)
        size = target.stat().st_size / 1e6
        print(f"{key}: {n} rows, {size:.1f} MB, {time.time() - start:.0f}s, {geom_types}", flush=True)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main(*sys.argv[1:])
