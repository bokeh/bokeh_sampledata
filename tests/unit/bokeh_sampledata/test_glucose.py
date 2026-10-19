# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.glucose as m

ALL = ("data",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_data() -> None:
    assert isinstance(m.data, pd.DataFrame)


def test_glucose_time_index_and_measurements() -> None:
    assert list(m.data.columns) == ["isig", "glucose"]
    assert isinstance(m.data.index, pd.DatetimeIndex)
    assert m.data.index.tz is None
    assert m.data.index.is_monotonic_increasing
    assert m.data.index[0] == pd.Timestamp("2010-03-24 09:51:00")
    assert pd.api.types.is_numeric_dtype(m.data["glucose"])
    assert m.data.iloc[0]["glucose"] == 258
