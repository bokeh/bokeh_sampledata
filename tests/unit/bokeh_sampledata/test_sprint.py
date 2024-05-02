# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.sprint as m

ALL = ("sprint",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_sprint() -> None:
    assert isinstance(m.sprint, pd.DataFrame)

    assert len(m.sprint) == 85
