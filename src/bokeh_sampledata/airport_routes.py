# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""US airport locations and observed domestic airline routes for July 2026.

Airport locations are public-domain `OurAirports <https://ourairports.com/data/>`_
records. Routes are derived from the U.S. Department of Transportation, Bureau
of Transportation Statistics, Reporting Carrier On-Time Performance data.
Source: https://www.transtats.bts.gov/

This sample selects completed, non-diverted July 2026 flights and retains
operating-carrier, origin, and destination combinations observed at least four
times. It is a historical sample, not a flight schedule or a complete network.
Reporting-carrier coverage excludes some smaller operators. Carrier identifiers
are DOT identifiers, rather than the old OpenFlights identifiers.

Airport identifiers are OurAirports identifiers, which differ from the previous
OpenFlights values. Join the two tables using their source/destination ID fields,
or use IATA codes for external joins. The BTS code ``PBI`` is matched to the
OurAirports record labeled ``DJT`` in this source snapshot. Time-zone, codeshare,
and equipment fields are unspecified. Data is public domain with source credit
retained. Source hashes and transformation details are in ``licenses/datasets.json``.

This module contains two pandas DataFrames, ``airports`` and ``routes``.

.. rubric:: ``airports``

:bokeh-dataframe:`bokeh.sampledata.airport_routes.airports`

.. rubric:: ``routes``

:bokeh-dataframe:`bokeh.sampledata.airport_routes.routes`

.. bokeh-sampledata-xref:: airport_routes

"""

from __future__ import annotations

from . import package_csv

__all__ = ("airports", "routes")

airports = package_csv("airports.csv", dtype={"Timezone": str, "DST": str, "TZ": str})

routes = package_csv("routes.csv.gz", dtype={"AirlineID": str, "Codeshare": str, "Equipment": str})
