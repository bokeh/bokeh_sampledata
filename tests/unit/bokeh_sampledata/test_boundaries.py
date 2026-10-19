# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Geographic records and permanent historical compatibility contracts."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from shapely.geometry.base import BaseGeometry

from bokeh_sampledata import package_path

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize(("name", "count"), [("us_states", 51), ("us_counties", 3233)])
def test_legacy_plotting_interface(name: str, count: int) -> None:
    import numpy as np

    module = importlib.import_module("bokeh_sampledata." + name)
    data = module.data
    assert isinstance(data, dict) and len(data) == count
    assert module.data is data
    for key, value in data.items():
        if name == "us_states":
            assert isinstance(key, str) and len(key) == 2
            assert set(value) == {"name", "region", "lats", "lons"}
        else:
            assert isinstance(key, tuple) and len(key) == 2
            assert all(isinstance(part, int) for part in key)
            assert set(value) == {"name", "detailed_name", "state", "lats", "lons"}
            assert value["state"] == value["state"].lower()
        assert isinstance(value["lats"], np.ndarray)
        assert isinstance(value["lons"], np.ndarray)
        assert value["lats"].dtype == value["lons"].dtype == np.float64
        assert len(value["lats"]) == len(value["lons"]) > 0
        assert np.array_equal(np.isnan(value["lats"]), np.isnan(value["lons"]))
    if name == "us_states":
        assert data["OR"]["name"] == "Oregon"
        assert data["OR"]["region"] == "Northwest"
        assert np.isnan(data["AK"]["lons"]).any()
    else:
        # The classic Texas example filters on lowercase state and accesses
        # tuple FIPS identifiers, metadata, and exterior coordinate arrays.
        texas = {key: value for key, value in data.items() if value["state"] == "tx"}
        assert len(texas) == 254
        assert data[(1, 1)]["name"] == "Autauga"
        assert data[(1, 1)]["detailed_name"] == "Autauga County, Alabama"
        assert data[(1, 1)]["lons"][0] == -86.41182
        assert data[(1, 1)]["lats"][0] == 32.4757


def test_lazy_legacy_attributes() -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            """
import bokeh_sampledata.us_states as states
import bokeh_sampledata.us_counties as counties
for module in (states, counties):
    assert 'data' not in vars(module)
    assert 'data' in dir(module)
    assert isinstance(module.data, dict)
    assert module.data is module.data
    try:
        module.missing
    except AttributeError:
        pass
    else:
        raise AssertionError('unknown attributes must raise')
from bokeh_sampledata.us_states import data
assert data is states.data
""",
        ],
        check=True,
    )


def test_records_do_not_parse_legacy() -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            """
import bokeh_sampledata.us_states as states
import bokeh_sampledata.us_counties as counties

def fail():
    raise AssertionError('legacy parser called')
for module in (states, counties):
    module._read_data = fail
    assert module.records()
    assert 'data' not in vars(module)
""",
        ],
        check=True,
    )


@pytest.mark.parametrize(
    ("name", "count", "fields", "identifier"),
    [
        ("us_states", 51, {"code", "name", "region", "geometry"}, "code"),
        (
            "us_counties",
            3233,
            {"fips", "state_fips", "county_fips", "state", "name", "detailed_name", "geometry"},
            "fips",
        ),
        ("world_countries", 242, {"id", "name", "iso_a2", "iso_a3", "continent", "region", "geometry"}, "id"),
    ],
)
def test_records(name: str, count: int, fields: set[str], identifier: str) -> None:
    from shapely.geometry import MultiPolygon, Polygon

    module = importlib.import_module("bokeh_sampledata." + name)
    records = module.records()
    assert len(records) == count
    ids = [record[identifier] for record in records]
    assert ids == sorted(set(ids))
    for record in records:
        assert set(record) == fields
        geometry = record["geometry"]
        assert isinstance(geometry, Polygon | MultiPolygon)
        assert geometry.is_valid and not geometry.is_empty
        if name == "us_counties":
            assert len(record["fips"]) == 5
            assert record["fips"] == record["state_fips"] + record["county_fips"]
        if name == "world_countries":
            assert record["iso_a2"] is None or len(record["iso_a2"]) == 2
            assert record["iso_a3"] is None or len(record["iso_a3"]) == 3
    assert {r["geometry"].geom_type for r in records} == {"Polygon", "MultiPolygon"}
    if name != "us_states":
        assert any(
            len(p.interiors)
            for r in records
            for p in (r["geometry"].geoms if isinstance(r["geometry"], MultiPolygon) else [r["geometry"]])
        )
    records[0]["name"] = "changed"
    assert module.records()[0]["name"] != "changed"


def test_state_filter_decodes_only_matches(monkeypatch: pytest.MonkeyPatch) -> None:
    import shapely

    from bokeh_sampledata import us_counties

    original = shapely.from_wkb
    calls: list[bytes] = []

    def decode(value: bytes) -> BaseGeometry:
        calls.append(value)
        return original(value)

    monkeypatch.setattr(shapely, "from_wkb", decode)
    tx = us_counties.records(state="TX")
    assert len(tx) == len(calls) == 254
    assert {r["state"] for r in tx} == {"TX"}
    assert {r["state_fips"] for r in tx} == {"48"}
    assert [r["fips"] for r in tx] == [r["fips"] for r in us_counties.records(state="tx")]
    assert len(us_counties.records(state="pr")) == 78
    assert us_counties.records(state="ZZ") == []
    invalid: Any
    for invalid in ["Texas", "48", " TX", "", "éé", 48]:
        with pytest.raises(ValueError, match="two-letter"):
            us_counties.records(state=invalid)
    with sqlite3.connect(package_path("geographic_boundaries.db")) as connection:
        plan = connection.execute("EXPLAIN QUERY PLAN SELECT geometry FROM us_counties WHERE state = ?", ("TX",))
        assert "us_counties_state" in str(plan.fetchall())


def test_packaged_manifest() -> None:
    path = package_path("geographic_boundaries.db")
    manifest = json.loads(path.with_suffix(".json").read_text())
    assert manifest["geometry_encoding"] == "WKB"
    assert path.stat().st_size == manifest["bytes"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest["sha256"]
    assert manifest["inputs"] == {
        "US_Counties.csv": "db5efb4678f92006ffdf4bad2a1b6decbb4bf0b91ba15dadcc103a2a04718708",
        "US_Regions_State_Boundaries.csv.gz": "6384a4be00b233adee9d30784485f45bc5afb0ad8d01ad874fc4abe5170ee665",
    }
    assert not package_path("US_Counties.csv").exists()
    assert not package_path("US_Regions_State_Boundaries.csv.gz").exists()


def test_no_geopandas_or_pyarrow() -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            """
import sys
sys.modules['geopandas'] = None
sys.modules['pyarrow'] = None
from bokeh_sampledata import us_states, us_counties, world_countries
assert us_states.records() and us_counties.records('TX') and world_countries.records()
""",
        ],
        check=True,
    )


@pytest.mark.skipif(
    "NATURAL_EARTH_ARCHIVE" not in os.environ, reason="regeneration requires the verified source archive"
)
def test_deterministic_generation(tmp_path: Path) -> None:
    # Opt-in regeneration test: no downloads or generation dependencies at runtime.
    output = tmp_path / "geographic_boundaries.db"
    command = [
        sys.executable,
        str(ROOT / "tools/generate_boundaries.py"),
        os.environ["NATURAL_EARTH_ARCHIVE"],
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, capture_output=True)
    first = output.read_bytes()
    subprocess.run(command, check=True, capture_output=True)
    assert output.read_bytes() == first == package_path("geographic_boundaries.db").read_bytes()


def test_shared_wkb_exteriors() -> None:
    import shapely
    from shapely.geometry import MultiPolygon, Polygon

    from bokeh_sampledata._boundaries import exterior_coordinates

    polygon = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)], [[(1, 1), (2, 1), (1, 2)]])
    other = Polygon([(10, 10), (12, 10), (12, 12)])
    lons, lats = exterior_coordinates(shapely.to_wkb(MultiPolygon([polygon, other]), byte_order=1))
    assert lons[:5] == [0, 4, 4, 0, 0]
    assert lats[:5] == [0, 0, 4, 4, 0]
    import math

    assert math.isnan(lons[5]) and math.isnan(lats[5])
    assert lons[6:] == [10, 12, 12, 10]
    assert lats[6:] == [10, 10, 12, 10]
