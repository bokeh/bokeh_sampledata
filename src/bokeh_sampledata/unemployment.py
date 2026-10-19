# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Per-county unemployment data for United States in 2009.

License: `Public Domain`_

Sourced from the U.S. Bureau of Labor Statistics. Current program and
historical data information: https://www.bls.gov/lau/

The ``by_fips`` dictionary maps five-character county FIPS strings, such as
``"01001"``, to unemployment rates. It joins directly to the ``fips`` field in
``us_counties.records()``. Rates are percentages.

.. code-block:: python

    from bokeh_sampledata import unemployment, us_counties

    counties = us_counties.records(state="AL")
    rates = [unemployment.by_fips.get(county["fips"]) for county in counties]

County boundaries and identifiers can change over time, so some records may
have no matching 2009 rate.

The existing ``data`` dictionary remains available with the same tuple keys
and values.

The dict is indexed by the two-tuples containing ``(state_id, county_id)`` and
has the unemployment rate (2009) as the value.

.. code-block:: ipython

    {
        (1, 1): 9.7,
        (1, 3): 9.1,
        ...
    }

.. bokeh-sampledata-xref:: unemployment

"""

from __future__ import annotations

import csv
import gzip

from . import package_path

__all__ = ("by_fips", "data")

data = {}

with gzip.open(package_path("unemployment09.csv.gz"), "rt", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    for row in reader:
        _, state_id, county_id, _, _, _, _, _, rate = row
        data[(int(state_id), int(county_id))] = float(rate)

by_fips = {f"{state_id:02d}{county_id:03d}": rate for (state_id, county_id), rate in data.items()}
