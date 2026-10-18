# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Natural Earth 1:50m Admin 0 countries, version 5.1.1.

Boundaries reflect de facto control, not necessarily legal claims. The source
is public domain. See ``docs/geographic_boundaries.md`` in the source
distribution for examples and provenance, and ``tools/README.md`` for
regeneration. Source terms also ship in ``_data/geographic_boundaries.LICENSE.txt``.
"""

from __future__ import annotations

from typing import cast

from ._boundaries import CountryRecord, read_records

__all__ = ("records",)


def records() -> list[CountryRecord]:
    """Return 242 country/territory records in Natural Earth ADM0_A3 order.

    ``id`` is the unique source ADM0_A3 identifier; ``iso_a2``/``iso_a3`` are
    source ISO_A2_EH/ISO_A3_EH codes, or None for -99 (these may be shared
    or unofficial, e.g. XK for Kosovo). Geometry is
    a Shapely Polygon/MultiPolygon in longitude/latitude degrees (WGS84).
    Other keys are ``name`` (English country/territory name), ``continent``,
    and ``region`` (Natural Earth's UN-style region). Parts and holes are
    preserved; all geometries are valid and nonempty. Each call returns
    fresh records.
    """
    return cast(list[CountryRecord], read_records("world_countries"))
