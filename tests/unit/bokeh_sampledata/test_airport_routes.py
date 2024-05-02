# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.airport_routes as m

ALL = (
    "airports",
    "routes",
)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_airports() -> None:
    assert isinstance(m.airports, pd.DataFrame)


def test_routes() -> None:
    assert isinstance(m.routes, pd.DataFrame)
