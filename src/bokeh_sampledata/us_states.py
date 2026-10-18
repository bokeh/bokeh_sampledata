# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Geometry data for US States.

The permanent ``data`` dictionary is loaded on first access.
Use ``records()`` for Shapely-native polygons and metadata (requires the
``geometry`` extra).

The data is indexed by the two letter state code (e.g., 'CA', 'TX') and has the
following structure:

.. code-block:: python

    In [4]: data["OR"]
    Out[4]:
    {
        'name': 'Oregon',
        'region': 'Northwest',
        'lats': [46.29443, ..., 46.26068],
        'lons': [-124.03622, ..., -124.15935]
    }

.. bokeh-sampledata-xref:: us_states

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

    Coordinates are longitude/latitude degrees (WGS84). Requires the
    ``geometry`` extra. Each call returns fresh records; ``data`` is independent.
    """
    return cast(list[StateRecord], read_records("us_states"))
