# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Daily weather at six U.S. airports.

License: `CC BY 4.0`_

The CSV covers July 1, 2014 through June 30, 2015. The stations are
Houston Hobby (KHOU), Jacksonville (KJAX), Chicago Midway
(KMDW), Philadelphia (KPHL), Phoenix Sky Harbor (KPHX), and Seattle-Tacoma
(KSEA).

The CSV contains these columns:

* ``airport`` is the ICAO airport code. ``date`` is the date in ``YYYY-MM-DD`` format.
* ``actual_mean_temp``, ``actual_min_temp``, and ``actual_max_temp`` are observed
  temperatures in degrees Fahrenheit.
* ``average_min_temp`` and ``average_max_temp`` are historical averages for
  that day of the year, in degrees Fahrenheit.
* ``record_min_temp`` and ``record_max_temp`` are historical records for
  that day of the year, in degrees Fahrenheit. ``record_min_temp_year``
  and ``record_max_temp_year`` give the years when those records occurred.
* ``actual_precipitation``, ``average_precipitation``, and
  ``record_precipitation`` are precipitation amounts in inches.

FiveThirtyEight published the data in
`U.S. Weather History <https://github.com/fivethirtyeight/data/tree/master/us-weather-history>`_
using observations and historical statistics from Weather Underground.
Bokeh combined the airport files and standardized the dates to ISO format.

.. bokeh-sampledata-xref:: airport_weather

"""

from __future__ import annotations

from . import package_path

__all__ = ("csv_path",)

csv_path = package_path("airport_weather.csv")
