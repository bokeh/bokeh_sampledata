# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pytest

import bokeh_sampledata.stocks as m

ALL = (
    "AAPL",
    "FB",
    "GOOG",
    "IBM",
    "MSFT",
)


def test___all__() -> None:
    assert m.__all__ == ALL


@pytest.mark.parametrize("name", ["AAPL", "FB", "GOOG", "IBM", "MSFT"])
def test_data(name: str) -> None:
    data = getattr(m, name)
    assert isinstance(data, dict)
