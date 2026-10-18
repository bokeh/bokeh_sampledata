# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.commits as m

ALL = ("data",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_data() -> None:
    assert isinstance(m.data, pd.DataFrame)
    assert len(m.data) == 4916


def test_commit_timezone_and_local_clock_times() -> None:
    assert list(m.data.columns) == ["day", "time"]
    assert isinstance(m.data.index, pd.DatetimeIndex)
    assert str(m.data.index.tz) == "US/Central"
    assert m.data.index[0] == pd.Timestamp("2017-04-22 20:11:58", tz="UTC")
    assert m.data["time"].tolist() == m.data.index.time.tolist()
