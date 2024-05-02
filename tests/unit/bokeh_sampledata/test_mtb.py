# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.mtb as m

ALL = ("obiszow_mtb_xcm",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_obiszow_mtb_xcm() -> None:
    assert isinstance(m.obiszow_mtb_xcm, pd.DataFrame)

    assert len(m.obiszow_mtb_xcm) == 978
