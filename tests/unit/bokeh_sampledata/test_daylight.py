# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.daylight as m

ALL = ("daylight_warsaw_2013",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_daylight_warsaw_2013() -> None:
    assert isinstance(m.daylight_warsaw_2013, pd.DataFrame)

    assert len(m.daylight_warsaw_2013) == 365
