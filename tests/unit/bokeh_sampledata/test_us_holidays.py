# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import bokeh_sampledata.us_holidays as m

ALL = ("us_holidays",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_us_holidays() -> None:
    assert isinstance(m.us_holidays, list)

    assert len(m.us_holidays) == 305
