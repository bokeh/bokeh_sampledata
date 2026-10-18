# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Provide historical ticker data for selected stocks.

License: `Public Domain`_.

Sourced from `Quandl WIKI Prices`_, using an `archived copy`_. Quandl declared
the data public domain and permitted redistribution in its `publisher notice`_.
The values are provided as supplied by the source.

The series end on March 1, 2013. Open, high, low, close, and volume are
unadjusted. ``adj_close`` contains the source's split- and dividend-adjusted
closing prices, including adjustments for corporate actions after this period.
The ``GOOG`` dictionary contains Google's pre-2014 history, filed under
``GOOGL`` in the source.

The ``data`` pandas DataFrame contains all five series, with columns ``ticker``,
``date``, ``open``, ``high``, ``low``, ``close``, ``volume``, and ``adj_close``.
Dates are parsed as pandas timestamps. Rows are ordered by ticker, then date.
The DataFrame is constructed on first access.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.stocks.data`

The module also contains five dicts: ``AAPL``, ``FB``, ``GOOG``, ``IBM``, and ``MSFT``.

Each dictionary has the structure:

.. code-block:: python

    AAPL['date']       # list of date string
    AAPL['open']       # list of float
    AAPL['high']       # list of float
    AAPL['low']        # list of float
    AAPL['close']      # list of float
    AAPL['volume']     # list of int
    AAPL['adj_close']  # list of float

.. bokeh-sampledata-xref:: stocks

.. _Quandl WIKI Prices: https://data.nasdaq.com/databases/WIKIP
.. _archived copy: https://www.kaggle.com/datasets/marketneutral/quandl-wiki-prices-us-equites/versions/1
.. _publisher notice: https://web.archive.org/web/20150411011214/https://www.quandl.com/data/WIKI

"""

from __future__ import annotations

import csv
import gzip
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    import pandas as pd

from . import package_path

# -----------------------------------------------------------------------------
# Globals and constants
# -----------------------------------------------------------------------------

__all__ = (
    "AAPL",
    "FB",
    "GOOG",
    "IBM",
    "MSFT",
    "data",
)

_TICKERS = ("AAPL", "FB", "GOOG", "IBM", "MSFT")

if TYPE_CHECKING:
    data: pd.DataFrame


def __getattr__(name: str) -> object:
    if name != "data":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    import pandas as pd

    frames = []
    for ticker in _TICKERS:
        frame = pd.DataFrame(globals()[ticker])
        frame.insert(0, "ticker", ticker)
        frames.append(frame)
    data = pd.concat(frames, ignore_index=True)
    data["date"] = pd.to_datetime(data["date"])
    globals()["data"] = data
    return data


# -----------------------------------------------------------------------------
# General API
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Dev API
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Private API
# -----------------------------------------------------------------------------


class StockData(TypedDict):
    date: list[str]
    open: list[float]
    high: list[float]
    low: list[float]
    close: list[float]
    volume: list[int]
    adj_close: list[float]


def _read_data() -> dict[str, StockData]:
    filename = package_path("stocks.csv.gz")
    stocks = {
        name: StockData(date=[], open=[], high=[], low=[], close=[], volume=[], adj_close=[]) for name in _TICKERS
    }
    with gzip.open(filename, "rt", encoding="utf-8", newline="") as f:
        next(f)
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            ticker, date, open_price, high, low, close, volume, adj_close = row
            data = stocks[ticker]
            data["date"].append(date)
            data["open"].append(float(open_price))
            data["high"].append(float(high))
            data["low"].append(float(low))
            data["close"].append(float(close))
            data["volume"].append(int(volume))
            data["adj_close"].append(float(adj_close))
    return stocks


_stocks = _read_data()
AAPL = _stocks["AAPL"]
FB = _stocks["FB"]
GOOG = _stocks["GOOG"]
IBM = _stocks["IBM"]
MSFT = _stocks["MSFT"]
del _stocks
