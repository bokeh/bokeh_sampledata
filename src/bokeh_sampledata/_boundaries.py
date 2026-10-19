# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Shared readers for packaged geographic records and legacy plotting arrays."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from typing import TYPE_CHECKING, Any, TypedDict

from . import package_path

if TYPE_CHECKING:
    from shapely.geometry import MultiPolygon, Polygon


class StateRecord(TypedDict):
    code: str
    name: str
    region: str
    geometry: Polygon | MultiPolygon


class CountyRecord(TypedDict):
    fips: str
    state_fips: str
    county_fips: str
    state: str
    name: str
    detailed_name: str
    geometry: Polygon | MultiPolygon


class CountryRecord(TypedDict):
    id: str
    name: str
    iso_a2: str | None
    iso_a3: str | None
    continent: str
    region: str
    geometry: Polygon | MultiPolygon


def read_records(table: str, state: str | None = None) -> list[Any]:
    from shapely import from_wkb

    if table not in {"us_states", "us_counties", "world_countries"}:
        raise ValueError(f"Unknown boundary table: {table}")
    query = f"SELECT metadata, geometry FROM {table}"
    parameters: tuple[str, ...] = ()
    if state is not None:
        query += " WHERE state = ?"
        parameters = (state,)
    query += " ORDER BY id"
    uri = package_path("geographic_boundaries.db").as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        return [
            dict(json.loads(metadata), geometry=from_wkb(wkb))
            for metadata, wkb in connection.execute(query, parameters)
        ]


def exterior_coordinates(wkb: bytes) -> tuple[list[float], list[float]]:
    """Extract polygon exteriors, separating parts with NaNs and omitting holes."""
    from shapely import from_wkb
    from shapely.geometry import MultiPolygon, Polygon

    geometry = from_wkb(wkb)
    if not isinstance(geometry, Polygon | MultiPolygon):
        raise ValueError("Expected polygon boundary geometry")
    polygons = [geometry] if isinstance(geometry, Polygon) else geometry.geoms
    lons: list[float] = []
    lats: list[float] = []
    for polygon in polygons:
        if lons:
            lons.append(float("nan"))
            lats.append(float("nan"))
        x, y = polygon.exterior.xy
        lons.extend(x)
        lats.extend(y)
    return lons, lats


def read_legacy(table: str) -> dict[Any, Any]:
    """Construct compatible plotting dictionaries from the shared WKB geometry."""
    import numpy as np

    if table not in {"us_states", "us_counties"}:
        raise ValueError(f"Unknown legacy table: {table}")
    uri = package_path("geographic_boundaries.db").as_uri() + "?mode=ro"
    result = {}
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        rows = connection.execute(f"SELECT metadata, geometry FROM {table} ORDER BY ordinal")
        for metadata, wkb in rows:
            record = json.loads(metadata)
            lons, lats = exterior_coordinates(wkb)
            if table == "us_states":
                key = record["code"]
                value = dict(name=record["name"], region=record["region"])
            else:
                key = (int(record["state_fips"]), int(record["county_fips"]))
                value = dict(name=record["name"], detailed_name=record["detailed_name"], state=record["state"].lower())
            value.update(lats=np.array(lats, dtype=np.float64), lons=np.array(lons, dtype=np.float64))
            result[key] = value
    return result
