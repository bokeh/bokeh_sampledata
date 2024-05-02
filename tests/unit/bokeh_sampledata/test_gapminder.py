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
