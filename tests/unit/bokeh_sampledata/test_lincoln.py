# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

from bokeh_sampledata.lincoln import data


def test_daily_2016_temperatures() -> None:
    assert list(data.columns) == ["STATION", "NAME", "DATE", "TMAX", "TMIN"]
    dates = pd.to_datetime(data["DATE"], format="%Y-%m-%d")
    assert dates.tolist() == pd.date_range("2016-01-01", "2016-12-31").tolist()
    assert set(data["STATION"]) == {"USW00094996"}
    for column in ("TMAX", "TMIN"):
        assert pd.api.types.is_numeric_dtype(data[column])
        assert data[column].isna().sum() == 1
    complete = data.dropna(subset=["TMAX", "TMIN"])
    assert (complete["TMAX"] >= complete["TMIN"]).all()
    assert data.iloc[0]["TMAX"] == 36.0
    assert data.iloc[0]["TMIN"] == 15.0
