# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd
import pytest

from bokeh_sampledata.cows import data


def test_butterfat_by_breed_and_age() -> None:
    assert data.shape == (100, 3)
    assert list(data.columns) == ["butterfat", "age", "breed"]
    assert pd.api.types.is_numeric_dtype(data["butterfat"])
    assert not data.isna().any().any()
    assert set(data["breed"]) == {"Ayrshire", "Canadian", "Guernsey", "Holstein-Friesian", "Jersey"}
    assert set(data["age"]) == {"Mature", "2 years old"}
    assert data.iloc[0]["butterfat"] == pytest.approx(3.74)
    assert data.iloc[0]["breed"] == "Ayrshire"
