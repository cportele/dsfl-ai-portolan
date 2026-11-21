#!/usr/bin/env python3
"""Derive one SQL query per feature type from the ldproxy feature providers.

The queries return every version (voorkomen) of every object with the property names of the
API, so the GeoParquet files have the same columns as the collections of the APIs. Output is a
JSON manifest that export.py reads.

Mapping of the provider sourcePaths:
- column                                  -> t.column
- [EXPRESSION]{sql=...}                   -> the expression, with $T$ = t
- [a=b]table{sortKey=s}/column            -> array of the column (VALUE_ARRAY, FEATURE_REF_ARRAY)
- [a=b]table{sortKey=s} with properties   -> FEATURE_REF_ARRAY: array of the ids;
                                             OBJECT_ARRAY: JSON array of objects
- FEATURE_REF with properties id/title    -> the id only
- constantValue (objecttype)              -> left out, the collection is the object type
- GEOMETRY                                -> arcs approximated by line segments (GeoParquet has no
                                             curves), max. deviation 1 mm

Usage: gen_sql.py <providers dir> <manifest.json>
"""

import json
import re
import sys
from pathlib import Path

import yaml

PROVIDERS = ["bag", "bgt", "wijkenbuurten", "postcode6"]

CURVE_TYPES = "('CIRCULARSTRING','COMPOUNDCURVE','CURVEPOLYGON','MULTICURVE','MULTISURFACE')"

JOIN_RE = re.compile(r"^\[(\w+)=(\w+)\](\w+)(?:\{sortKey=(\w+)\})?(?:/(\w+))?$")
TABLE_RE = re.compile(r"^/(\w+)(?:\{.*\})?$")
REF_API_RE = re.compile(r"/(\w+)/collections/\w+/")
EXPR_RE = re.compile(r"^\[EXPRESSION\]\{sql=(.*)\}$", re.S)


def q(name):
    return '"' + name.replace('"', '""') + '"'


def linear(expr):
    return (
        f"CASE WHEN GeometryType({expr}) IN {CURVE_TYPES} "
        f"THEN ST_CurveToLine({expr}, 0.001, 1, 1) ELSE {expr} END"
    )


def value_expr(sp, alias):
    m = EXPR_RE.match(sp)
    if m:
        return "(" + m.group(1).replace("$T$", alias) + ")"
    return f"{alias}.{q(sp)}"


def ref_id(prop):
    """sourcePath of the id of a FEATURE_REF(_ARRAY) with nested id/title."""
    return prop["properties"]["id"]["sourcePath"]


def json_member(name, prop, alias):
    t = prop.get("type")
    if t == "FEATURE_REF" and "properties" in prop:
        return f"'{name}', {value_expr(ref_id(prop), alias)}"
    if t == "GEOMETRY":
        # RD coordinates in mm, no crs member (GeoJSON has none; the CRS is the one of the file)
        geom = linear(alias + "." + q(prop["sourcePath"]))
        return f"'{name}', ST_AsGeoJSON({geom}, 3, 0)::jsonb"
    return f"'{name}', {value_expr(prop['sourcePath'], alias)}"


def column_sql(name, prop, schema):
    t = prop.get("type")
    sp = prop.get("sourcePath", "")
    m = JOIN_RE.match(sp)
    if m:
        a, b, table, sort, col = m.groups()
        order = f" ORDER BY j.{q(sort)}" if sort else ""
        src = f"FROM {schema}.{q(table)} j WHERE j.{q(b)} = t.{q(a)}"
        if col:
            return f"(SELECT array_agg(j.{q(col)}{order}) {src})"
        if t == "FEATURE_REF_ARRAY":
            return f"(SELECT array_agg(j.{q(ref_id(prop))}{order}) {src})"
        if t == "OBJECT_ARRAY":
            members = ", ".join(json_member(n, p, "j") for n, p in prop["properties"].items())
            return f"(SELECT jsonb_agg(jsonb_build_object({members}){order}) {src})::text"
        raise ValueError(f"unsupported join {name}: {sp}")
    if t == "FEATURE_REF" and "properties" in prop:
        return value_expr(ref_id(prop), "t")
    if t == "GEOMETRY":
        return linear(f"t.{q(sp)}")
    if sp:
        return value_expr(sp, "t")
    raise ValueError(f"no sourcePath for {name}")


def ref_api(prop, api):
    """API of the referenced type: from refUriTemplate (other APIs), else the same API."""
    m = REF_API_RE.search(prop.get("refUriTemplate", ""))
    return m.group(1) if m else (api if prop.get("refType") else None)


def parquet_type(prop):
    t = prop.get("type")
    return {
        "VALUE_ARRAY": f"array<{prop.get('valueType', 'STRING').lower()}>",
        "FEATURE_REF_ARRAY": "array<string>",
        "OBJECT_ARRAY": "json",
        "FEATURE_REF": "string",
    }.get(t, (t or "STRING").lower())


def main(providers_dir, manifest_path):
    out = []
    for api in PROVIDERS:
        provider = yaml.safe_load((Path(providers_dir) / f"{api}.yml").read_text())
        schema = provider["connectionInfo"]["schemas"][0]
        for type_name, ty in provider["types"].items():
            table = TABLE_RE.match(ty["sourcePath"]).group(1)
            cols, meta, geoms = [], [], []
            for name, prop in ty["properties"].items():
                if "constantValue" in prop:
                    continue
                cols.append(f"{column_sql(name, prop, schema)} AS {q(name)}")
                if prop.get("type") == "GEOMETRY":
                    geoms.append({"name": name, "primary": prop.get("role") == "PRIMARY_GEOMETRY"})
                meta.append(
                    {
                        "name": name,
                        "type": parquet_type(prop),
                        "label": prop.get("label"),
                        "description": prop.get("description"),
                        "featureRef": prop.get("type", "").startswith("FEATURE_REF"),
                        "refType": prop.get("refType"),
                        "refApi": ref_api(prop, api),
                        "role": prop.get("role"),
                        "codelist": (prop.get("constraints") or {}).get("codelist"),
                    }
                )
            sql = "SELECT " + ",\n  ".join(cols) + f"\nFROM {schema}.{q(table)} t"
            out.append(
                {
                    "api": api,
                    "type": type_name,
                    "table": f"{schema}.{table}",
                    "label": ty.get("label"),
                    "description": ty.get("description"),
                    "geometries": geoms,
                    "columns": meta,
                    "sql": sql,
                }
            )
    Path(manifest_path).write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"{len(out)} feature types -> {manifest_path}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
