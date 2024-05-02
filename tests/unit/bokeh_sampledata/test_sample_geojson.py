# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import bokeh_sampledata.sample_geojson as m

ALL = ("geojson",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_geojson() -> None:
    assert isinstance(m.geojson, str)
