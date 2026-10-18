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
        count = connection.execute("SELECT count(*) FROM omdb").fetchone()[0]
        assert count >= 10000
        assert connection.execute("SELECT count(*) FROM tomatoes").fetchone() == (count,)
        assert connection.execute("SELECT count(*) FROM omdb JOIN tomatoes USING (ID)").fetchone() == (count,)
        movie = connection.execute(
            "SELECT Title, Year, tomatoes.Rating FROM omdb JOIN tomatoes USING (ID) "
            "WHERE tomatoes.Rating IS NOT NULL LIMIT 1"
        ).fetchone()
        assert movie is not None
        title, year, rating = movie
        assert isinstance(title, str) and title
        assert isinstance(year, int)
        assert 0 <= rating <= 10
        assert connection.execute("SELECT Rating, Meter, Reviews FROM tomatoes LIMIT 1").fetchone() is not None


def test_movie_explorer_default_selection() -> None:
    with sqlite3.connect(m.movie_path.as_uri() + "?mode=ro", uri=True) as connection:
        rows = connection.execute(
            "SELECT Title, Meter, Reviews, BoxOffice FROM omdb JOIN tomatoes USING (ID) "
            "WHERE Reviews >= 80 AND Year BETWEEN 1970 AND 2014"
        ).fetchall()
        assert len(rows) >= 100
        assert all("[demo metrics]" not in row[0] for row in rows)
        assert len({row[1] for row in rows}) >= 30
        assert len({row[3] for row in rows}) >= 100
        assert connection.execute("SELECT count(*) FROM omdb WHERE Director != ''").fetchone()[0] >= 100


def test_cast_filter_has_real_names() -> None:
    with sqlite3.connect(m.movie_path.as_uri() + "?mode=ro", uri=True) as connection:
        assert connection.execute("SELECT count(*) FROM omdb WHERE [Cast] != ''").fetchone()[0] >= 500
        assert connection.execute("SELECT count(*) FROM omdb WHERE [Cast] LIKE '%Tom Hanks%'").fetchone()[0] >= 1


def test_unavailable_fields_remain_null_for_compatibility() -> None:
    with sqlite3.connect(m.movie_path.as_uri() + "?mode=ro", uri=True) as connection:
        for table, columns in {
            "omdb": ("imdbRating", "imdbVotes"),
            "tomatoes": ("Image", "Consensus", "userMeter", "userRating", "userReviews", "DVD", "Website"),
        }.items():
            for column in columns:
                assert connection.execute(f'SELECT count(*) FROM {table} WHERE "{column}" IS NOT NULL').fetchone() == (
                    0,
                )
        for column in ("Genre", "Director", "Cast"):
            assert connection.execute(f'SELECT count(*) FROM omdb WHERE "{column}" IS NULL').fetchone() == (0,)


def test_movie_explorer_filters() -> None:
    with sqlite3.connect(m.movie_path.as_uri() + "?mode=ro", uri=True) as connection:
        for condition in (
            "Genre LIKE '%Sci-Fi%'",
            "Genre LIKE '%Animation%'",
            "Genre LIKE '%Biography%'",
            "Genre LIKE '%History%'",
            "[Cast] LIKE '%Tom Hanks%'",
            "[Cast] LIKE '%Meryl Streep%'",
            "Year = 2014",
            "Oscars >= 4",
        ):
            assert (
                connection.execute(
                    "SELECT count(*) FROM omdb JOIN tomatoes USING (ID) WHERE Reviews >= 10 AND " + condition
                ).fetchone()[0]
                > 0
            )
        assert connection.execute("SELECT [Cast] FROM omdb WHERE ID = 201674").fetchone()[0].find("Meryl Streep") >= 0
