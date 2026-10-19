# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd
import pytest

from bokeh_sampledata.forensic_glass import data


def test_mineral_measurements_and_glass_types() -> None:
    assert data.shape == (214, 10)
    assert list(data.columns) == ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "type"]
    assert all(pd.api.types.is_numeric_dtype(data[column]) for column in data.columns[:-1])
    assert not data.isna().any().any()
    assert set(data["type"]) == {"WinF", "WinNF", "Veh", "Con", "Tabl", "Head"}
    assert data.iloc[0]["Si"] == pytest.approx(71.78)
    assert data.iloc[0]["type"] == "WinF"
