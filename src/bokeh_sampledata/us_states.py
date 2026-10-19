# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Geometry records for US states and the District of Columbia.

``records()`` returns 51 dictionaries in state-code order, each containing
``code`` (uppercase postal abbreviation), ``name``, ``region``, and ``geometry``
(a Shapely Polygon or MultiPolygon). Shapely is a standard package dependency.

.. code-block:: python

    from bokeh_sampledata.us_states import records

    states = records()
    oregon = next(state for state in states if state["code"] == "OR")
    geometry = oregon["geometry"]

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
The packaged ``licenses/geographic-boundaries.txt`` contains the source
links, comparison evidence, attribution, and remaining provenance uncertainties.

Invalid geometry in Alaska is repaired using Shapely ``make_valid``, retaining
polygonal components and discarding collapsed line/point remnants. Source
metadata is retained.

.. bokeh-sampledata-xref:: us_states

Legacy plotting data
~~~~~~~~~~~~~~~~~~~~

The historical ``data`` attribute is retained for compatibility. New code
should use ``records()``. It is loaded and cached on first access, independently
of ``records()``. Importing the module performs no boundary I/O.

``data`` maps two-letter state codes to dictionaries containing ``name``,
``region``, ``lats``, and ``lons``. Coordinates are NumPy float64 arrays with NaN
separators between polygon exteriors. Interior holes are omitted. Both APIs
use the same geometry dataset, so repairs, ring ordering, and closing points
can change coordinates from the historical arrays.

.. code-block:: python

    from bokeh_sampledata.us_states import data

    oregon = data["OR"]
    latitudes = oregon["lats"]
    longitudes = oregon["lons"]

"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, cast

import numpy as np

from ._boundaries import StateRecord, read_legacy, read_records

if TYPE_CHECKING:
    from numpy.typing import NDArray

__all__ = ("data", "records")


class StateData(TypedDict):
    name: str
    region: str
    lats: NDArray[np.float64]
    lons: NDArray[np.float64]


def _read_data() -> dict[str, StateData]:
    return cast(dict[str, StateData], read_legacy("us_states"))


def __getattr__(name: str) -> object:
    if name == "data":
        value = _read_data()
        globals()["data"] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | {"data"})


if TYPE_CHECKING:
    data: dict[str, StateData]


def records() -> list[StateRecord]:
    """Return 51 state/DC records in code order, with Shapely geometry.

    Each dictionary has ``code`` (uppercase postal abbreviation), ``name``,
    ``region``, and ``geometry`` (Shapely Polygon or MultiPolygon). Parts and
    holes are preserved. All geometries are valid and nonempty.

    Coordinates retain the Census NAD83 longitude/latitude degrees without
    reprojection. Each call returns fresh records. ``data`` is independent.
    """
    return cast(list[StateRecord], read_records("us_states"))
