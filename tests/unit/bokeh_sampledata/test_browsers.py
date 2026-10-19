# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import struct

import pandas as pd

import bokeh_sampledata.browsers as m

ALL = (
    "browsers_nov_2013",
    "icons",
)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_browsers_nov_2013() -> None:
    assert isinstance(m.browsers_nov_2013, pd.DataFrame)
    assert len(m.browsers_nov_2013) == 118


def test_icons() -> None:
    assert isinstance(m.icons, dict)
    assert set(m.icons) == {"Chrome", "Firefox", "Safari", "Opera", "IE"}
    assert len(set(m.icons.values())) == 5
    for png in m.icons.values():
        assert png.startswith(b"\x89PNG\r\n\x1a\n")
        assert struct.unpack(">II", png[16:24]) == (32, 32)
        assert b"Copyright 2024 Fonticons, Inc." in png
        assert b"https://creativecommons.org/licenses/by/4.0/" in png
        assert b"https://github.com/FortAwesome/Font-Awesome/blob/6.7.2/svgs/brands/" in png


def test_browser_names_and_version_numbers() -> None:
    data = m.browsers_nov_2013.set_index("Version")
    assert list(data.columns) == ["Share", "Browser", "VersionNumber"]
    assert data.loc["Chrome 30.0", "Browser"] == "Chrome"
    assert data.loc["Chrome 30.0", "VersionNumber"] == "30.0"
    assert data.loc["Chrome 30.0", "Share"] == 18.51
    assert data.loc["Other", "Browser"] == "Other"
    assert data.loc["Other", "VersionNumber"] == "0"


def test_browser_shares() -> None:
    data = m.browsers_nov_2013
    assert abs(data["Share"].sum() - 100) < 0.1
    assert data["Share"].between(0, 100).all()
    assert set(m.icons) <= set(data["Browser"])


def test_donut_example_aggregation() -> None:
    shares = m.browsers_nov_2013.groupby("Browser")["Share"].sum()
    selected = shares[shares >= 1].copy()
    selected.loc["Other"] = shares[shares < 1].sum()
    assert abs(selected.sum() - 100) < 0.1
    assert selected.gt(0).all()
