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
