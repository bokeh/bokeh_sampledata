# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.cycling as c

ALL = ("cycling",)


def test___all__() -> None:
    assert c.__all__ == ALL


def test_cycling() -> None:
    assert isinstance(c.cycling, pd.DataFrame)

    assert len(c.cycling) == 4391
