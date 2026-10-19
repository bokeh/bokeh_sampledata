# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import bokeh_sampledata.unemployment as m
from bokeh_sampledata import us_counties

ALL = ("by_fips", "data")


def test___all__() -> None:
    assert m.__all__ == ALL


def test_data() -> None:
    assert isinstance(m.data, dict)


def test_fips_keys_and_values() -> None:
    assert len(m.by_fips) == len(m.data) == 3218
    assert all(len(fips) == 5 and fips.isascii() and fips.isdigit() for fips in m.by_fips)
    assert m.by_fips["01001"] == m.data[(1, 1)] == 9.7
    assert m.by_fips["01003"] == m.data[(1, 3)] == 9.1
    assert m.by_fips["72153"] == m.data[(72, 153)] == 16.0
    assert m.data == {(int(fips[:2]), int(fips[2:])): rate for fips, rate in m.by_fips.items()}


def test_fips_view_joins_county_records() -> None:
    counties = us_counties.records(state="AL")
    assert len(counties) == 67
    assert all(county["fips"] in m.by_fips for county in counties)
    autauga = next(county for county in counties if county["fips"] == "01001")
    assert m.by_fips[autauga["fips"]] == 9.7
