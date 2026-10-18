# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""GeoJSON locations for the 25 former NHS England area teams.

License: `Open Government Licence v2.0
<https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/>`_.
Contains public sector information licensed under the Open Government Licence v2.0.

Published by NHS Choices and converted to GeoJSON by Jeni Tennison in
https://github.com/JeniT/nhs-choices, revision ``7651daedf0`` (February 2014).
Names, addresses, and contact details are historical. These area teams were
subsequently reorganized. This sample retains the original 25 point features.

.. bokeh-sampledata-xref:: sample_geojson

"""

from __future__ import annotations

from . import package_path

__all__ = ("geojson",)

with open(package_path("sample_geojson.geojson"), encoding="utf-8") as f:
    geojson = f.read()
