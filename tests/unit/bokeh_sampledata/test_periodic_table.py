# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.periodic_table as m

ALL = ("elements",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_elements() -> None:
    assert isinstance(m.elements, pd.DataFrame)

    assert len(m.elements) == 118
