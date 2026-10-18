# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

from datetime import date
from math import isfinite

import pytest

import bokeh_sampledata.stocks as m

ALL = (
    "AAPL",
    "FB",
    "GOOG",
    "IBM",
    "MSFT",
    "data",
)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_combined_dataframe() -> None:
    import pandas as pd

    frame = m.data
    assert isinstance(frame, pd.DataFrame)
    assert frame is m.data
    assert list(frame.columns) == ["ticker", "date", "open", "high", "low", "close", "volume", "adj_close"]
    assert frame.index.equals(pd.RangeIndex(12154))
    assert pd.api.types.is_datetime64_any_dtype(frame["date"])
    assert pd.api.types.is_integer_dtype(frame["volume"])
    for ticker in ("AAPL", "FB", "GOOG", "IBM", "MSFT"):
        series = getattr(m, ticker)
        rows = frame[frame["ticker"] == ticker]
        assert rows["date"].dt.strftime("%Y-%m-%d").tolist() == series["date"]
        for column in ("open", "high", "low", "close", "volume", "adj_close"):
            assert rows[column].tolist() == series[column]


@pytest.mark.parametrize("name", ["AAPL", "FB", "GOOG", "IBM", "MSFT"])
def test_data(name: str) -> None:
    data = getattr(m, name)
    assert set(data) == {"date", "open", "high", "low", "close", "volume", "adj_close"}
    assert len({len(column) for column in data.values()}) == 1
    assert len(data["date"]) > 0
    dates = [date.fromisoformat(value) for value in data["date"]]
    assert dates == sorted(set(dates))
    assert dates[-1] == date(2013, 3, 1)
    for column in ("open", "high", "low", "close", "adj_close"):
        assert all(isinstance(value, float) and isfinite(value) and value > 0 for value in data[column])
    assert all(isinstance(value, int) and value >= 0 for value in data["volume"])
    assert all(
        low <= min(opening, closing) <= max(opening, closing) <= high
        for low, opening, closing, high in zip(data["low"], data["open"], data["close"], data["high"], strict=True)
    )
    assert all(day.weekday() < 5 for day in dates)
    expected_start = {
        "AAPL": "2000-03-01",
        "FB": "2012-05-18",
        "GOOG": "2004-08-19",
        "IBM": "2000-03-01",
        "MSFT": "2000-03-01",
    }
    assert data["date"][0] == expected_start[name]


@pytest.mark.parametrize(
    ("name", "count"), [("AAPL", 3270), ("FB", 196), ("GOOG", 2148), ("IBM", 3270), ("MSFT", 3270)]
)
def test_historical_trading_calendar(name: str, count: int) -> None:
    dates = getattr(m, name)["date"]
    assert len(dates) == count
    assert "2001-09-11" not in dates
    assert "2012-10-29" not in dates
    assert "2012-12-25" not in dates


@pytest.mark.parametrize(
    ("name", "first_close", "last_close"),
    [
        ("AAPL", 130.31, 430.47),
        ("FB", 38.2318, 27.78),
        ("GOOG", 100.335, 806.19),
        ("IBM", 100.25, 202.91),
        ("MSFT", 90.81, 27.95),
    ],
)
def test_source_prices(name: str, first_close: float, last_close: float) -> None:
    data = getattr(m, name)
    assert data["close"][0] == first_close
    assert data["close"][-1] == last_close


def test_adjusted_close() -> None:
    # Apple's archive includes splits and dividends after the selected dates.
    assert m.AAPL["adj_close"][0] == pytest.approx(4.186662803811)
    assert m.AAPL["adj_close"][-1] == pytest.approx(56.137353095488)
    assert m.FB["adj_close"] == m.FB["close"]
