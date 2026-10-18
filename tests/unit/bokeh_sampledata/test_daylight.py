# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

from datetime import date, time, timedelta

import pandas as pd

import bokeh_sampledata.daylight as m

ALL = ("daylight_warsaw_2013",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_daylight_warsaw_2013() -> None:
    assert isinstance(m.daylight_warsaw_2013, pd.DataFrame)

    assert len(m.daylight_warsaw_2013) == 365


def test_calendar_dates_and_clock_times() -> None:
    data = m.daylight_warsaw_2013
    assert list(data.columns) == ["Date", "Sunrise", "Sunset", "Summer"]
    assert all(type(value) is date for value in data["Date"])
    assert data["Date"].tolist() == [date(2013, 1, 1) + timedelta(days=n) for n in range(365)]
    for column in ("Sunrise", "Sunset"):
        assert all(type(value) is time for value in data[column])
    assert (data["Sunrise"] < data["Sunset"]).all()
    assert data.iloc[0]["Sunrise"] == time(7, 45)
    assert data.iloc[0]["Sunset"] == time(15, 34)
    assert data.iloc[-1]["Sunset"] == time(15, 32)
