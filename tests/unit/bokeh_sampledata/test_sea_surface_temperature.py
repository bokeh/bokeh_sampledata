# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.sea_surface_temperature as m

ALL = ("sea_surface_temperature",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_sea_surface_temperature() -> None:
    assert isinstance(m.sea_surface_temperature, pd.DataFrame)

    assert len(m.sea_surface_temperature) == 19226


def test_temperature_time_index_and_units() -> None:
    data = m.sea_surface_temperature
    assert list(data.columns) == ["temperature"]
    assert isinstance(data.index, pd.DatetimeIndex)
    assert data.index.name == "time"
    assert str(data.index.tz) == "UTC"
    assert data.index.is_monotonic_increasing
    assert data.index[0] == pd.Timestamp("2016-02-15", tz="UTC")
    assert pd.api.types.is_numeric_dtype(data["temperature"])
    assert data.iloc[0]["temperature"] == 4.929
