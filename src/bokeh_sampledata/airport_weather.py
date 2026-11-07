# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Daily weather for Houston Hobby, Chicago Midway, and Seattle-Tacoma.

The CSV covers July 1, 2014 through June 30, 2015. It includes observed,
historical average, and record temperatures in degrees Fahrenheit, plus
precipitation in inches. The ``airport`` column contains ICAO airport codes.

FiveThirtyEight published the data in
`U.S. Weather History <https://github.com/fivethirtyeight/data/tree/master/us-weather-history>`_
using observations and historical statistics from Weather Underground.
The dataset is available under
`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`_.
Bokeh combined the three airport files and standardized the dates to ISO format.

.. bokeh-sampledata-xref:: airport_weather

"""

from __future__ import annotations

from . import package_path

__all__ = ("csv_path",)

csv_path = package_path("airport_weather.csv")
