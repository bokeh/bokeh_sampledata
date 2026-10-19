# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd
import pytest

from bokeh_sampledata.penguins import data


def test_penguin_measurements_and_missing_values() -> None:
    measurements = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    assert data.shape == (344, 7)
    assert list(data.columns) == ["species", "island", *measurements, "sex"]
    assert set(data["species"]) == {"Adelie", "Chinstrap", "Gentoo"}
    assert set(data["island"]) == {"Torgersen", "Biscoe", "Dream"}
    assert set(data["sex"].dropna()) == {"MALE", "FEMALE"}
    assert data["sex"].isna().sum() == 11
    for column in measurements:
        assert pd.api.types.is_numeric_dtype(data[column])
        assert data[column].isna().sum() == 2
        assert (data[column].dropna() > 0).all()
    assert data.iloc[0]["bill_length_mm"] == pytest.approx(39.1)
    assert data.iloc[0]["species"] == "Adelie"
