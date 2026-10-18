# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Geometry records for Natural Earth countries and territories.

``records()`` returns 242 dictionaries in Natural Earth ``ADM0_A3`` order.
Each contains ``id``, ``name`` (English country/territory name), ``iso_a2``,
``iso_a3``, ``continent``, ``region`` (Natural Earth's UN-style region), and
``geometry`` (a Shapely Polygon or MultiPolygon). Shapely is a standard
package dependency.

.. code-block:: python

    from bokeh_sampledata.world_countries import records

    countries = records()
    geometry = countries[0]["geometry"]

Coordinates are WGS84 longitude/latitude degrees without reprojection.
Polygon parts and interior holes are preserved. All geometries are valid and
nonempty, with no validity repairs needed. Each call returns fresh dictionaries
and geometries. Importing the module performs no boundary I/O. The public API
is independent of the packaged storage format.

``id`` is the unique source ``ADM0_A3`` identifier. ``iso_a2`` and ``iso_a3``
use the source ``ISO_A2_EH`` and ``ISO_A3_EH`` fields, with ``-99`` represented
as ``None``. These source codes can be shared by multiple territories and
include unofficial codes such as ``XK`` for Kosovo. Use ``id`` as the unique
key. These fields provide ``FR``, ``NO``, and ``TW`` where the primary source
ISO fields have missing values or an alternative code.

Source and license
~~~~~~~~~~~~~~~~~~

Geometry comes from `Natural Earth Admin 0 countries, 1:50m, version 5.1.1
<https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/>`_.
Boundaries are provided as represented in the Natural Earth source data.
See the source's `boundary policy
<https://www.naturalearthdata.com/about/disputed-boundaries-policy/>`_.

Natural Earth data is `public domain
<https://www.naturalearthdata.com/about/terms-of-use/>`_, including commercial
use and redistribution. Attribution is not required. These terms are compatible
with distributing the dataset alongside BSD-3-Clause software. The Natural
Earth data itself remains public domain.

Source terms and provenance also ship in
``_data/geographic_boundaries.LICENSE.txt``. Storage and regeneration
instructions are in ``tools/README.md`` in the source distribution.

"""

from __future__ import annotations

from typing import cast

from ._boundaries import CountryRecord, read_records

__all__ = ("records",)


def records() -> list[CountryRecord]:
    """Return 242 country/territory records in Natural Earth ADM0_A3 order.

    ``id`` is the unique source ADM0_A3 identifier. ``iso_a2``/``iso_a3`` are
    source ISO_A2_EH/ISO_A3_EH codes, or None for -99 (these may be shared
    or unofficial, e.g. XK for Kosovo). Geometry is
    a Shapely Polygon/MultiPolygon in longitude/latitude degrees (WGS84).
    Other keys are ``name`` (English country/territory name), ``continent``,
    and ``region`` (Natural Earth's UN-style region). Parts and holes are
    preserved. All geometries are valid and nonempty. Each call returns
    fresh records.
    """
    return cast(list[CountryRecord], read_records("world_countries"))
