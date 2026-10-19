# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.cycling as c

ALL = ("cycling",)


def test___all__() -> None:
    assert c.__all__ == ALL


def test_cycling() -> None:
    assert isinstance(c.cycling, pd.DataFrame)

    assert len(c.cycling) == 4391
    expected_columns = {
        "position_lat",
        "position_long",
        "altitude",
        "power",
        "cadence",
        "distance",
        "speed",
        "time",
    }
    assert set(c.cycling.columns) == expected_columns


def test_elapsed_workout_times() -> None:
    elapsed = c.cycling["time"]
    assert pd.api.types.is_timedelta64_dtype(elapsed)
    assert elapsed.is_monotonic_increasing
    assert elapsed.iloc[0] == pd.Timedelta(0)
    assert elapsed.iloc[-1] > pd.Timedelta(0)
    assert all(pd.api.types.is_numeric_dtype(c.cycling[column]) for column in c.cycling.columns if column != "time")
