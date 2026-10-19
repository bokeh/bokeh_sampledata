# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

from datetime import date

import bokeh_sampledata.us_holidays as m

ALL = ("us_holidays",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_us_holidays() -> None:
    assert isinstance(m.us_holidays, list)

    assert len(m.us_holidays) == 723


def test_calendar_rules_and_range() -> None:
    events = m.us_holidays
    assert events == sorted(set(events))
    assert min(day.year for day, _ in events) == 1999
    assert max(day.year for day, _ in events) == 2030
    assert (date(2024, 3, 31), "Easter Sunday") in events
    assert (date(2024, 11, 28), "Thanksgiving Day (US-OPM)") in events
    assert (date(2021, 6, 18), "Juneteenth National Independence Day (US-OPM)") in events
    assert not any(day.year < 2021 and name.startswith("Juneteenth") for day, name in events)


def test_calendar_example_federal_filter() -> None:
    holidays = [(day, name) for day, name in m.us_holidays if day.year == 2013 and "(US-OPM)" in name]
    assert len(holidays) == 10
    assert (date(2013, 12, 25), "Christmas Day (US-OPM)") in holidays


def test_observed_weekend_and_easter_dates() -> None:
    assert (date(2015, 7, 3), "Independence Day (US-OPM)") in m.us_holidays
    assert (date(1999, 12, 31), "New Year's Day (US-OPM)") in m.us_holidays
    assert (date(2024, 3, 29), "Good Friday") in m.us_holidays
    assert (date(2024, 2, 14), "Ash Wednesday") in m.us_holidays
