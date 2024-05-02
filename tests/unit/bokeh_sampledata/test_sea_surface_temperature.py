# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.sea_surface_temperature as m

ALL = ("sea_surface_temperature",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_sea_surface_temperature() -> None:
    assert isinstance(m.sea_surface_temperature, pd.DataFrame)

    assert len(m.sea_surface_temperature) == 19226
