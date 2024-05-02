# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.perceptions as m

ALL = (
    "numberly",
    "probly",
)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_numberly() -> None:
    assert isinstance(m.numberly, pd.DataFrame)

    assert len(m.numberly) == 46


def test_probly() -> None:
    assert isinstance(m.probly, pd.DataFrame)

    assert len(m.probly) == 46
