# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Calculate annual sunrise and sunset times for a location.

License: BSD-3-Clause.

These illustrative calculations follow the NOAA `Solar Calculator
<https://gml.noaa.gov/grad/solcalc/calcdetails.html>`_ spreadsheet equations
(after Meeus, *Astronomical Algorithms*), a level horizon, and a 90.833-degree solar zenith
for the conventional solar-radius and atmospheric-refraction correction.
Times are rounded to the nearest minute. They are calculated estimates, not
observations or precise almanac predictions.

.. rubric:: ``daylight_for_year``

Calculate a DataFrame for a year from 1901 through 2099, using an IANA time zone:

.. code-block:: python

    from bokeh_sampledata.daylight import daylight_for_year

    daylight = daylight_for_year(
        2026, latitude=52.2297, longitude=21.0122, timezone="Europe/Warsaw",
    )

The columns are ``Date`` (local calendar date), ``Sunrise`` and ``Sunset``
(local clock times), and ``Summer`` (1 when daylight saving applies at local
noon, otherwise 0). A missing sunrise or sunset, such as during polar day or
night, is represented by ``None``. Leap years and time-zone transitions follow
the calendar and IANA time-zone database. Skipped local dates are omitted.
Sunsets after midnight belong to that local calendar date. If a date contains
multiple sunrises or sunsets, the first chronological event is retained.
Both events may be absent during either polar day or polar night.

.. rubric:: ``daylight_warsaw_2013``

The existing example DataFrame is calculated for Warsaw at 52.2297 degrees north,
21.0122 degrees east, in ``Europe/Warsaw``. Its name and column types are retained.

:bokeh-dataframe:`bokeh.sampledata.daylight.daylight_warsaw_2013`

.. bokeh-sampledata-xref:: daylight

"""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta, timezone as dt_timezone
from math import acos, asin, cos, degrees, floor, isfinite, radians, sin, tan
from zoneinfo import ZoneInfo

import pandas as pd

__all__ = ("daylight_for_year", "daylight_warsaw_2013")


def _julian_day(moment: datetime) -> float:
    # Days since J2000.0 epoch (2000-01-01 12:00 UTC) plus 2451545.0.
    j2000 = datetime(2000, 1, 1, 12, tzinfo=dt_timezone.utc)
    return 2451545.0 + (moment - j2000).total_seconds() / 86400


def _sun_position(moment: datetime) -> tuple[float, float]:
    """Return (declination in radians, equation of time in minutes), per the
    NOAA Solar Calculator spreadsheet (Meeus, Astronomical Algorithms)."""
    t = (_julian_day(moment) - 2451545.0) / 36525
    mean_longitude = radians((280.46646 + t * (36000.76983 + t * 0.0003032)) % 360)
    anomaly = radians(357.52911 + t * (35999.05029 - 0.0001537 * t))
    eccentricity = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    center = (
        sin(anomaly) * (1.914602 - t * (0.004817 + 0.000014 * t))
        + sin(2 * anomaly) * (0.019993 - 0.000101 * t)
        + sin(3 * anomaly) * 0.000289
    )
    omega = radians(125.04 - 1934.136 * t)
    apparent_longitude = radians(degrees(mean_longitude) + center - 0.00569 - 0.00478 * sin(omega))
    mean_obliquity = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60
    obliquity = radians(mean_obliquity + 0.00256 * cos(omega))
    declination = asin(sin(obliquity) * sin(apparent_longitude))
    y = tan(obliquity / 2) ** 2
    equation_of_time = 4 * degrees(
        y * sin(2 * mean_longitude)
        - 2 * eccentricity * sin(anomaly)
        + 4 * eccentricity * y * sin(anomaly) * cos(2 * mean_longitude)
        - 0.5 * y * y * sin(4 * mean_longitude)
        - 1.25 * eccentricity * eccentricity * sin(2 * anomaly)
    )
    return declination, equation_of_time


def _solar_event(day: date, latitude: float, longitude: float, *, sunrise: bool) -> datetime | None:
    midnight = datetime(day.year, day.month, day.day, tzinfo=dt_timezone.utc)
    minutes = 720.0
    for _ in range(4):
        estimate = midnight + timedelta(minutes=minutes)
        declination, equation_of_time = _sun_position(estimate)
        cosine = cos(radians(90.833)) / (cos(latitude) * cos(declination)) - tan(latitude) * tan(declination)
        if not -1 <= cosine <= 1:
            return None
        hour_angle = degrees(acos(cosine))
        if not sunrise:
            hour_angle = -hour_angle
        minutes = 720 - 4 * (longitude + hour_angle) - equation_of_time
    return midnight + timedelta(minutes=floor(minutes + 0.5))


def daylight_for_year(year: int, *, latitude: float, longitude: float, timezone: str) -> pd.DataFrame:
    """Return daily sunrise, sunset, and daylight-saving flags for a location.

    Latitude is degrees north in [-90, 90], longitude is degrees east in
    [-180, 180], and timezone is an IANA name such as ``Europe/Warsaw``.
    Dates refer to the requested local calendar year. Clock times have no
    attached timezone, matching the existing example DataFrame. Events that
    do not occur on a local date are ``None``.

    Years must be between 1901 and 2099. Skipped local dates are omitted.
    If multiple events occur on a date, only the first of each kind is retained.

    The returned DataFrame is independent of ``daylight_warsaw_2013``.
    """
    if not isfinite(latitude) or not -90 <= latitude <= 90:
        raise ValueError("latitude must be finite and between -90 and 90 degrees")
    if not isfinite(longitude) or not -180 <= longitude <= 180:
        raise ValueError("longitude must be finite and between -180 and 180 degrees")
    if not 1901 <= year <= 2099:
        raise ValueError("year must be between 1901 and 2099")
    first = date(year, 1, 1)
    days = 366 if calendar.isleap(year) else 365
    zone = ZoneInfo(timezone)
    latitude_radians = radians(latitude)
    events: dict[tuple[date, bool], datetime] = {}
    # Events and local calendar dates may straddle UTC dates or the date line.
    for n in range(-2, days + 2):
        day = first + timedelta(days=n)
        for sunrise in (True, False):
            event = _solar_event(day, latitude_radians, longitude, sunrise=sunrise)
            if event is None:
                continue
            local = event.astimezone(zone)
            if local.year == year:
                key = (local.date(), sunrise)
                events[key] = min(event, events.get(key, event))
    rows = []
    for n in range(days):
        day = first + timedelta(days=n)
        noon = datetime(day.year, day.month, day.day, 12, tzinfo=zone)
        if noon.astimezone(dt_timezone.utc).astimezone(zone).date() != day:
            continue
        summer = int(bool(noon.dst()))
        sunrise_event = events.get((day, True))
        sunset_event = events.get((day, False))
        rows.append(
            (
                day,
                sunrise_event.astimezone(zone).time() if sunrise_event is not None else None,
                sunset_event.astimezone(zone).time() if sunset_event is not None else None,
                summer,
            )
        )
    return pd.DataFrame(rows, columns=("Date", "Sunrise", "Sunset", "Summer"))


daylight_warsaw_2013 = daylight_for_year(2013, latitude=52.2297, longitude=21.0122, timezone="Europe/Warsaw")
