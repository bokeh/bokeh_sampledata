# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Locations of US cities with more than 5000 residents.

License: `CC BY 3.0 <https://creativecommons.org/licenses/by/3.0/>`_

Sourced from https://www.geonames.org/export/ (subset of *cities5000.zip*)

This module contains one dict: ``data``.

.. code-block:: python

    data['lat']  # list of float
    data['lon']  # list of float

.. bokeh-sampledata-xref:: us_cities

"""

from __future__ import annotations

import gzip
import json

from . import package_path

__all__ = ("data",)

with gzip.open(package_path("us_cities.json.gz"), "rb") as f:
    data = json.load(f)
