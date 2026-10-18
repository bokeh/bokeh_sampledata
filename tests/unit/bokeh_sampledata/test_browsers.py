# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

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
    assert set(m.icons.keys()).issubset({"Chrome", "Firefox", "Safari", "Opera", "IE"})


def test_browser_names_and_version_numbers() -> None:
    data = m.browsers_nov_2013.set_index("Version")
    assert list(data.columns) == ["Share", "Browser", "VersionNumber"]
    assert data.loc["Chrome 30.0", "Browser"] == "Chrome"
    assert data.loc["Chrome 30.0", "VersionNumber"] == "30.0"
    assert data.loc["Chrome 30.0", "Share"] == 18.51
    assert data.loc["Pale Moon 24.0", "Browser"] == "Pale Moon"
    assert data.loc["Pale Moon 24.0", "VersionNumber"] == "24.0"
    assert data.loc["Other", "Browser"] == "Other"
    assert data.loc["Other", "VersionNumber"] == "0"
