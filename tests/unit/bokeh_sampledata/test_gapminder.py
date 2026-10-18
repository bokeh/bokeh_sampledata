# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd
import pytest

import bokeh_sampledata.gapminder as m

ALL = (
    "fertility",
    "life_expectancy",
    "population",
    "regions",
)


def test___all__() -> None:
    assert m.__all__ == ALL


@pytest.mark.parametrize("name", ["fertility", "life_expectancy", "population", "regions"])
def test_data(name: str) -> None:
    data = getattr(m, name)
    assert isinstance(data, pd.DataFrame)


def test_country_and_year_alignment() -> None:
    years = [str(year) for year in range(1964, 2014)]
    for frame in (m.fertility, m.life_expectancy, m.population):
        assert frame.shape == (244, 50)
        assert frame.index.name == "Country"
        assert frame.index.is_unique
        assert frame.index.equals(m.fertility.index)
        assert frame.columns.tolist() == years
        assert all(pd.api.types.is_numeric_dtype(dtype) for dtype in frame.dtypes)
    assert m.fertility.loc["United States", "1964"] == pytest.approx(3.222)
    assert m.fertility.loc["United States", "2013"] == pytest.approx(1.976)


def test_regions_align_by_country_label() -> None:
    assert m.regions.index.is_unique
    assert set(m.regions.index) == set(m.fertility.index)
    assert list(m.regions.columns) == ["Group", "ID"]
    # The source region table has a different row order from the numeric tables.
    aligned = m.regions.reindex(m.fertility.index)
    assert aligned.loc["United States"].to_dict() == {"Group": "America", "ID": "US"}
    assert aligned.loc["China", "Group"] == "East Asia & Pacific"
