# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import os
import subprocess
import sys
from datetime import date, time, timedelta

import pandas as pd
import pytest

import bokeh_sampledata.daylight as m


def test___all__() -> None:
    assert m.__all__ == ("daylight_for_year", "daylight_warsaw_2013")


def test_legacy_dataframe() -> None:
    data = m.daylight_warsaw_2013
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["Date", "Sunrise", "Sunset", "Summer"]
    assert data["Date"].tolist() == [date(2013, 1, 1) + timedelta(days=n) for n in range(365)]
    assert all(type(value) is date for value in data["Date"])
    for column in ("Sunrise", "Sunset"):
        assert all(type(value) is time for value in data[column])
    assert (data["Sunrise"] < data["Sunset"]).all()
    assert time(7, 40) <= data.iloc[0]["Sunrise"] <= time(7, 50)
    assert time(15, 25) <= data.iloc[0]["Sunset"] <= time(15, 40)
    june = data.loc[data["Date"] == date(2013, 6, 21)].iloc[0]
    assert time(4, 10) <= june["Sunrise"] <= time(4, 20)
    assert time(20, 55) <= june["Sunset"] <= time(21, 10)
    assert data.loc[data["Summer"] == 1, "Date"].tolist() == [date(2013, 3, 31) + timedelta(days=n) for n in range(210)]


def test_leap_year_and_southern_seasons() -> None:
    data = m.daylight_for_year(2024, latitude=-33.8688, longitude=151.2093, timezone="Australia/Sydney")
    assert len(data) == 366
    assert date(2024, 2, 29) in data["Date"].tolist()
    january = data.iloc[0]
    june = data.loc[data["Date"] == date(2024, 6, 21)].iloc[0]
    assert january["Sunrise"] < june["Sunrise"]
    assert january["Sunset"] > june["Sunset"]
    assert january["Summer"] == 1
    assert june["Summer"] == 0


@pytest.mark.parametrize("latitude", [-90, -80, 80, 90])
def test_polar_missing_events(latitude: float) -> None:
    data = m.daylight_for_year(2024, latitude=latitude, longitude=0, timezone="UTC")
    for day in (date(2024, 6, 21), date(2024, 12, 21)):
        row = data.loc[data["Date"] == day].iloc[0]
        assert row["Sunrise"] is None
        assert row["Sunset"] is None


def test_date_line_local_dates() -> None:
    data = m.daylight_for_year(2024, latitude=1.8721, longitude=-157.4278, timezone="Pacific/Kiritimati")
    assert data.iloc[0]["Date"] == date(2024, 1, 1)
    assert data.iloc[-1]["Date"] == date(2024, 12, 31)
    assert data["Sunrise"].notna().all()
    assert data["Sunset"].notna().all()
    assert all(time(5) < value < time(8) for value in data["Sunrise"])
    assert all(time(17) < value < time(20) for value in data["Sunset"])
    assert not data["Summer"].any()


@pytest.mark.parametrize(
    ("coordinate", "value"),
    [("latitude", 91), ("latitude", float("nan")), ("longitude", -181), ("longitude", float("inf"))],
)
def test_invalid_coordinates(coordinate: str, value: float) -> None:
    coordinates = {"latitude": 0.0, "longitude": 0.0, coordinate: value}
    with pytest.raises(ValueError, match=coordinate):
        m.daylight_for_year(2024, timezone="UTC", **coordinates)


def test_independent_frames() -> None:
    data = m.daylight_for_year(2013, latitude=52.2297, longitude=21.0122, timezone="Europe/Warsaw")
    pd.testing.assert_frame_equal(data, m.daylight_warsaw_2013)
    data.loc[0, "Summer"] = 9
    assert m.daylight_warsaw_2013.loc[0, "Summer"] == 0


def test_skipped_local_date() -> None:
    data = m.daylight_for_year(2011, latitude=-13.8333, longitude=-171.75, timezone="Pacific/Apia")
    assert len(data) == 364
    assert date(2011, 12, 30) not in data["Date"].tolist()


@pytest.mark.parametrize("year", [1900, 2100])
def test_supported_year_range(year: int) -> None:
    with pytest.raises(ValueError, match="year"):
        m.daylight_for_year(year, latitude=0, longitude=0, timezone="UTC")


@pytest.mark.parametrize(
    ("latitude", "longitude", "day", "sunrise", "sunset"),
    [
        (52.2297, 21.0122, date(2013, 1, 1), time(6, 45), time(14, 34)),
        (69.6492, 18.9553, date(2024, 2, 1), time(8, 27), time(13, 30)),
    ],
)
def test_usno_reference_events(latitude: float, longitude: float, day: date, sunrise: time, sunset: time) -> None:
    # Independent USNO annual UTC tables, retrieved 2026-10-18.
    # https://aa.usno.navy.mil/data/RS_OneYear
    data = m.daylight_for_year(day.year, latitude=latitude, longitude=longitude, timezone="UTC")
    row = data.loc[data["Date"] == day].iloc[0]
    for column, expected in (("Sunrise", sunrise), ("Sunset", sunset)):
        actual = row[column]
        assert actual is not None
        delta = (actual.hour * 60 + actual.minute - expected.hour * 60 - expected.minute + 720) % 1440 - 720
        assert abs(delta) <= 1


def test_timezones_without_system_database() -> None:
    subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "from bokeh_sampledata.daylight import daylight_warsaw_2013; assert len(daylight_warsaw_2013) == 365",
        ],
        env={**os.environ, "PYTHONTZPATH": ""},
        check=True,
    )
