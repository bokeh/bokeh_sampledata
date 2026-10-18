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
)


def test___all__() -> None:
    assert m.__all__ == ALL


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
    assert all(high >= low for high, low in zip(data["high"], data["low"], strict=True))
    expected = {
        "AAPL": ("2000-03-01", 130.31),
        "FB": ("2012-05-18", 38.23),
        "GOOG": ("2004-08-19", 100.34),
        "IBM": ("2000-03-01", 100.25),
        "MSFT": ("2000-03-01", 90.81),
    }
    first_date, first_close = expected[name]
    assert data["date"][0] == first_date
    assert data["close"][0] == pytest.approx(first_close)
