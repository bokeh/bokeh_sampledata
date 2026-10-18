# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd
import pytest

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
        assert not m.autompg_clean["mfr"].isin([x]).any()


@pytest.mark.parametrize(
    ("spelling", "manufacturer"),
    [
        ("chevy", "chevrolet"),
        ("chevroelt", "chevrolet"),
        ("maxda", "mazda"),
        ("mercedes-benz", "mercedes"),
        ("toyouta", "toyota"),
        ("vokswagen", "volkswagen"),
        ("vw", "volkswagen"),
        ("ford", "ford"),
    ],
)
def test_manufacturer_normalization(spelling: str, manufacturer: str) -> None:
    raw = pd.DataFrame({"name": [f"{spelling} model"], "origin": [1], "mpg": [25.0]})
    original = raw.copy(deep=True)
    cleaned = m._clean_data(raw)
    assert cleaned["mfr"].tolist() == [manufacturer]
    assert cleaned["origin"].tolist() == ["North America"]
    assert cleaned["name"].equals(raw["name"])
    assert cleaned["mpg"].equals(raw["mpg"])
    pd.testing.assert_frame_equal(raw, original)


def test_origin_labels_preserve_row_order() -> None:
    raw = pd.DataFrame({"name": ["ford a", "toyota b", "vw c"], "origin": [1, 3, 2]}, index=[5, 2, 9])
    cleaned = m._clean_data(raw)
    assert cleaned.index.tolist() == [5, 2, 9]
    assert cleaned["origin"].tolist() == ["North America", "Asia", "Europe"]
    assert "mfr" not in raw.columns
    assert raw["origin"].tolist() == [1, 3, 2]
