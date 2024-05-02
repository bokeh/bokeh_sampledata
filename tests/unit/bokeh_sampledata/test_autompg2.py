# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.autompg2 as m

ALL = ("autompg2",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_autompg2() -> None:
    assert isinstance(m.autompg2, pd.DataFrame)
    assert len(m.autompg2) == 234
