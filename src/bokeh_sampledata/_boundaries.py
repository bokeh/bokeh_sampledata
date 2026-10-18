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
import zlib
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
    try:
        from shapely import from_wkb
    except ImportError as error:
        raise ImportError("Boundary records require Shapely >=2. Install bokeh_sampledata[geometry].") from error

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
            dict(json.loads(metadata), geometry=from_wkb(zlib.decompress(wkb)))
            for metadata, wkb in connection.execute(query, parameters)
        ]


def exterior_coordinates(wkb: bytes) -> tuple[list[float], list[float]]:
    """Decode exterior rings from our fixed little-endian 2D polygon WKB.

    This deliberately small reader supports only the two types produced by our
    generator, keeping the historical API independent of Shapely.
    """
    import struct

    offset = 0
    lons: list[float] = []
    lats: list[float] = []

    def uint() -> int:
        nonlocal offset
        value: int = struct.unpack_from("<I", wkb, offset)[0]
        offset += 4
        return value

    def geometry() -> None:
        nonlocal offset
        if wkb[offset] != 1:
            raise ValueError("Expected little-endian boundary WKB")
        offset += 1
        kind = uint()
        if kind == 6:
            for _ in range(uint()):
                geometry()
        elif kind == 3:
            if lons:
                lons.append(float("nan"))
                lats.append(float("nan"))
            for ring in range(uint()):
                count = uint()
                if ring == 0:
                    for x, y in struct.iter_unpack("<dd", wkb[offset : offset + count * 16]):
                        lons.append(x)
                        lats.append(y)
                offset += count * 16
        else:
            raise ValueError(f"Unsupported boundary WKB type: {kind}")

    geometry()
    if offset != len(wkb):
        raise ValueError("Trailing boundary WKB data")
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
            lons, lats = exterior_coordinates(zlib.decompress(wkb))
            if table == "us_states":
                key = record["code"]
                value = dict(name=record["name"], region=record["region"])
            else:
                key = (int(record["state_fips"]), int(record["county_fips"]))
                value = dict(name=record["name"], detailed_name=record["detailed_name"], state=record["state"].lower())
            value.update(lats=np.array(lats, dtype=np.float64), lons=np.array(lons, dtype=np.float64))
            result[key] = value
    return result
