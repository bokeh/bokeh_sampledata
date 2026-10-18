# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Geometry records for US counties and county equivalents.

``records()`` returns 3,233 dictionaries in FIPS order, each containing
``fips`` (five-digit string), ``state_fips`` (two-digit string), ``county_fips``
(three-digit string), ``state`` (uppercase postal abbreviation), ``name``,
``detailed_name``, and ``geometry`` (a Shapely Polygon or MultiPolygon).
Shapely is a standard package dependency.

.. code-block:: python

    from bokeh_sampledata.us_counties import records

    counties = records()
    texas = records(state="TX")
    geometry = texas[0]["geometry"]

The optional ``state`` argument accepts two-letter ASCII postal abbreviations
in either case, including DC and territories. Filtering uses an index before
geometry decoding. Unknown two-letter codes return an empty list. Names,
numeric FIPS codes, whitespace, and other formats raise ``ValueError``.
For example, Autauga County has ``fips="01001"``, ``state_fips="01"``, and
``county_fips="001"``.

Coordinates retain the Census NAD83 longitude/latitude degrees without
reprojection. Polygon parts and interior holes are preserved. All geometries
are valid and nonempty. Each call returns fresh dictionaries and geometries.

Source and license
~~~~~~~~~~~~~~~~~~

Geometry comes from Bokeh's historical boundary samples. Coordinate comparison
identifies simplified Census TIGER/Line geometry matching the official 2009
release at the source rounding precision. The exact acquisition vintage and
export intermediary remain unrecorded. These are historical samples.

The Census source metadata permits use and redistribution with acknowledgement
to the Census Bureau. Source: U.S. Census Bureau, TIGER/Line Shapefiles.
These terms are compatible with distribution alongside BSD-3-Clause software.
The packaged ``LICENSE-geographic-boundaries.txt`` contains the source
links, comparison evidence, attribution, and remaining provenance uncertainties.

Invalid geometry in 45 counties is repaired using Shapely ``make_valid``,
retaining polygonal components and discarding collapsed line/point remnants.
The packaged ``geographic_boundaries.json`` manifest records their identifiers.
Source metadata, including character replacement artifacts, is retained.
Sixteen duplicate Puerto Rico FIPS rows use the last source row, matching the
legacy dictionary.

.. bokeh-sampledata-xref:: us_counties

Legacy plotting data
~~~~~~~~~~~~~~~~~~~~

The historical ``data`` attribute is retained for compatibility. New code
should use ``records()``. It is loaded and cached on first access, independently
of ``records()``. Importing the module performs no boundary I/O.

``data`` maps numeric ``(state_id, county_id)`` tuples to dictionaries containing
``name``, ``detailed_name``, ``state`` (lowercase postal abbreviation), ``lats``,
and ``lons``. Names can repeat within a state. The combination of
``detailed_name`` and ``state`` is unique. Coordinates are NumPy float64 arrays
with NaN separators between polygon exteriors. Interior holes are omitted. Both APIs
use the same geometry dataset, so repairs, ring ordering, and closing points
can change coordinates from the historical arrays.

.. code-block:: python

    from bokeh_sampledata.us_counties import data

    autauga = data[(1, 1)]
    latitudes = autauga["lats"]
    longitudes = autauga["lons"]

"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, cast

import numpy as np

from ._boundaries import CountyRecord, read_legacy, read_records

if TYPE_CHECKING:
    from numpy.typing import NDArray

__all__ = ("data", "records")

# -----------------------------------------------------------------------------
# General API
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Dev API
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Private API
# -----------------------------------------------------------------------------


class CountyData(TypedDict):
    name: str
    detailed_name: str
    state: str
    lats: NDArray[np.float64]
    lons: NDArray[np.float64]


def _read_data() -> dict[tuple[int, int], CountyData]:
    return cast(dict[tuple[int, int], CountyData], read_legacy("us_counties"))


def __getattr__(name: str) -> object:
    if name == "data":
        value = _read_data()
        globals()["data"] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | {"data"})


if TYPE_CHECKING:
    data: dict[tuple[int, int], CountyData]


def records(state: str | None = None) -> list[CountyRecord]:
    """Return county records in padded FIPS order, with Shapely geometry.

    ``state`` accepts a two-letter postal abbreviation, case-insensitively
    (including DC and territories). Unknown two-letter codes return an empty
    list. Names, numeric FIPS codes, whitespace, and other formats raise
    ``ValueError``. Filtering uses an index before geometry decoding.

    Each dictionary has ``fips`` (five-digit string), ``state_fips`` (two
    digits), ``county_fips`` (three digits), ``state`` (uppercase postal code),
    ``name``, ``detailed_name``, and ``geometry`` (Shapely Polygon or
    MultiPolygon). Parts and holes are preserved. All geometries are valid
    and nonempty.

    Coordinates retain the Census NAD83 longitude/latitude degrees without
    reprojection. Each call returns fresh records. ``data`` is independent.
    """
    if state is not None:
        if not isinstance(state, str) or len(state) != 2 or not state.isascii() or not state.isalpha():
            raise ValueError("state must be a two-letter postal abbreviation")
        state = state.upper()
    return cast(list[CountyRecord], read_records("us_counties", state))
