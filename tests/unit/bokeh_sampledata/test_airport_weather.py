# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

from collections import defaultdict
from csv import DictReader
from datetime import date, timedelta

from bokeh_sampledata.airport_weather import csv_path


def test_airport_weather_daily_series() -> None:
    dates_by_airport: dict[str, list[date]] = defaultdict(list)
    with csv_path.open(encoding="utf-8", newline="") as file:
        for row in DictReader(file):
            dates_by_airport[row["airport"]].append(date.fromisoformat(row["date"]))
            for kind in ("actual", "average", "record"):
                assert int(row[f"{kind}_min_temp"]) <= int(row[f"{kind}_max_temp"])

    assert set(dates_by_airport) == {"KHOU", "KJAX", "KMDW", "KPHL", "KPHX", "KSEA"}
    expected = [date(2014, 7, 1) + timedelta(days=offset) for offset in range(365)]
    for dates in dates_by_airport.values():
        assert sorted(dates) == expected
