# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""A fixed worldwide snapshot of measured airport winds and weather.

License: public domain under the `NOAA/NWS reuse terms
<https://www.weather.gov/disclaimer>`_. Source credit is retained.

The 5,091 station reports were obtained from the `NOAA Aviation Weather Center
METAR cache <https://aviationweather.gov/data/api/#cache>`_ on November 18, 2026.
Observation times range from 20:25 to 21:51 UTC on that date. This is one report
per station, not a time series or a gridded field. Calm winds, variable-direction
winds, and missing measurements are preserved. Missing directions are not north.

This module contains one pandas DataFrame, ``data``, with these columns:

* ``station`` is the station identifier and ``time`` is a UTC timestamp.
* ``latitude`` and ``longitude`` are geographic coordinates in degrees.
* ``direction`` is the bearing wind comes from, clockwise from true north.
  A value of 360 means north. Missing values include variable-direction reports.
* ``speed`` and ``gust`` are wind speeds in knots.
* ``temperature`` and ``dewpoint`` are in degrees Celsius.
* ``elevation`` is station elevation in meters.

Invalid coordinate pairs and the elevation sentinel 9999 are stored as missing
values. Other reported values are retained without interpolation or imputation.
This is a Bokeh-curated extract, not a live feed or an official NOAA product. Original
source hashes, the column mapping, and reuse terms are recorded in
``licenses/datasets.json``. The curation script is
``tools/curate_wind_observations.py``.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.wind_observations.data`

.. bokeh-sampledata-xref:: wind_observations

"""

from __future__ import annotations

from . import package_csv

__all__ = ("data",)

data = package_csv("wind_observations.csv.gz", parse_dates=["time"])
