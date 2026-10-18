# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd
import pytest

from bokeh_sampledata.emissions import data


def test_country_year_emissions() -> None:
    assert data.shape == (10526, 3)
    assert list(data.columns) == ["country", "year", "emissions"]
    assert all(pd.api.types.is_numeric_dtype(data[column]) for column in ("year", "emissions"))
    assert not data.isna().any().any()
    assert not data.duplicated(["country", "year"]).any()
    assert data["year"].min() == 1950
    assert data["year"].max() == 2012
    afghanistan = data.loc[(data["country"] == "Afghanistan") & (data["year"] == 1950)]
    assert afghanistan["emissions"].item() == pytest.approx(0.010345801)
