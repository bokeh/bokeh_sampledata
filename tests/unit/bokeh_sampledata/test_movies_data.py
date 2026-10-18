# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import sqlite3
from pathlib import Path

import bokeh_sampledata.movies_data as m

ALL = ("movie_path",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_movie_path() -> None:
    assert isinstance(m.movie_path, Path)


def test_movie_database_queries() -> None:
    assert m.movie_path.is_file()
    with sqlite3.connect(m.movie_path.as_uri() + "?mode=ro", uri=True) as connection:
        assert connection.execute("PRAGMA quick_check").fetchall() == [("ok",)]
        assert connection.execute("SELECT count(*) FROM omdb").fetchone() == (12569,)
        assert connection.execute("SELECT count(*) FROM tomatoes").fetchone() == (76430,)
        movie = connection.execute(
            "SELECT Title, Year, imdbRating FROM omdb WHERE imdbRating IS NOT NULL LIMIT 1"
        ).fetchone()
        assert movie is not None
        title, year, rating = movie
        assert isinstance(title, str) and title
        assert isinstance(year, int)
        assert 0 <= rating <= 10
        assert connection.execute("SELECT Rating, Meter, Reviews FROM tomatoes LIMIT 1").fetchone() is not None
