# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.population as m

ALL = ("data",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_data() -> None:
    assert isinstance(m.data, pd.DataFrame)


def test_population_pyramid_contract() -> None:
    data = m.data
    assert list(data.columns) == ["LocID", "Location", "Year", "Sex", "AgeGrp", "AgeGrpStart", "Value"]
    assert not data.isna().any().any()
    assert set(data.Sex) == {"Male", "Female"}
    assert data.Value.ge(0).all()
    assert data.Year.between(1950, 2100).all()
    assert not data.duplicated(["Location", "Year", "Sex", "AgeGrp"]).any()
    assert data.groupby(["Location", "Year"]).size().eq(42).all()
    world = data[(data.Location == "World") & (data.Year == 2010)]
    assert world.Value.sum() == 7021732152
    assert data.Value.dtype == "float64"
    usa = data[data.Location == "United States of America"]
    assert set(usa.LocID) == {840}
    assert set(usa.Year) == set(range(1950, 2101, 5))
    world_years = data.loc[data.Location == "World", "Year"].unique()
    assert sum(world_years <= 2010) == 13
    assert len(world_years) == 31
