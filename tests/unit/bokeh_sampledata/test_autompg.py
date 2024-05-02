# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.autompg as m

ALL = (
    "autompg",
    "autompg_clean",
)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_autompg() -> None:
    assert isinstance(m.autompg, pd.DataFrame)
    assert len(m.autompg) == 392
    assert all(x in [1, 2, 3] for x in m.autompg.origin)


def test_autompg_clean() -> None:
    assert isinstance(m.autompg_clean, pd.DataFrame)
    assert len(m.autompg_clean) == 392
    assert all(x in ["North America", "Europe", "Asia"] for x in m.autompg_clean.origin)
    for x in ["chevy", "chevroelt", "maxda", "mercedes-benz", "toyouta", "vokswagen", "vw"]:
        assert x not in m.autompg_clean.mfr
