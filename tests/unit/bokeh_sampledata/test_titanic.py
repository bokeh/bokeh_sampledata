# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

from bokeh_sampledata.titanic import data


def test_passenger_demographics_and_survival() -> None:
    assert data.shape == (1313, 5)
    assert list(data.columns) == ["name", "class", "age", "sex", "survived"]
    assert pd.api.types.is_numeric_dtype(data["age"])
    assert pd.api.types.is_integer_dtype(data["survived"])
    assert data["age"].isna().sum() == 557
    assert (data["age"].dropna() >= 0).all()
    assert set(data["survived"]) == {0, 1}
    assert set(data["sex"]) == {"female", "male"}
    assert set(data["class"]) == {"1st", "2nd", "3rd", "*"}
    passenger = data.loc[data["name"] == "Allen, Miss Elisabeth Walton"].iloc[0]
    assert passenger["age"] == 29
    assert passenger["survived"] == 1
