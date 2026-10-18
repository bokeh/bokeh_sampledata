# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""This modules exposes geometry data for Unites States.

The permanent ``data`` dictionary is loaded on first access.
Use ``records()`` for Shapely-native polygons and metadata.

The data is indexed by two-tuples of ``(state_id, county_id)`` that
have the following dictionaries as values:

.. code-block:: ipython

    In [25]: data[(1,1)]
    Out[25]:
    {
        'name': 'Autauga',
        'detailed name': 'Autauga County, Alabama',
        'state': 'al',
        'lats': [32.4757, ..., 32.48112],
        'lons': [-86.41182, ..., -86.41187]
    }

Entries for ``'name'`` can have duplicates for certain states (e.g. Virginia).
The combination of ``'detailed name'`` and ``'state'`` will always be unique.

.. bokeh-sampledata-xref:: us_counties

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
    list; names, numeric FIPS codes, whitespace, and other formats raise
    ``ValueError``. Filtering uses an index before geometry decoding.

    Coordinates retain the Census NAD83 longitude/latitude degrees without
    reprojection. Each call returns fresh records; ``data`` is independent.
    """
    if state is not None:
        if not isinstance(state, str) or len(state) != 2 or not state.isascii() or not state.isalpha():
            raise ValueError("state must be a two-letter postal abbreviation")
        state = state.upper()
    return cast(list[CountyRecord], read_records("us_counties", state))
