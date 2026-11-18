# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

from bokeh_sampledata.wind_observations import data


def test_wind_observations_snapshot() -> None:
    assert len(data) == 5091
    assert data.station.is_unique
    assert data.station.is_monotonic_increasing
    assert str(data.time.dt.tz) == "UTC"
    assert data.time.min() == pd.Timestamp("2026-11-18T20:25:00Z")
    assert data.time.max() == pd.Timestamp("2026-11-18T21:51:00Z")
    assert data.latitude.dropna().between(-90, 90).all()
    assert data.longitude.dropna().between(-180, 180).all()
    assert data.direction.dropna().between(0, 360).all()
    assert (data.speed.dropna() >= 0).all()
    assert (data.speed == 0).any()
    assert data.direction.isna().any()
    assert data.gust.isna().any()
    assert data.loc[data.station == "KSEA", "speed"].notna().all()
