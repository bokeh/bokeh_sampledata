# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

from pathlib import Path

import bokeh_sampledata.movies_data as m

ALL = ("movie_path",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_movie_path() -> None:
    assert isinstance(m.movie_path, Path)
