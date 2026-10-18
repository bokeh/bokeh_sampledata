# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Film information from Wikidata for the movie explorer example.

License: `CC0`_.

The dataset contains 17,472 films released from 1940 through 2014, selected from
`Wikidata`_ structured data with review-score statements. The snapshot was
retrieved on October 18, 2026. Values are provided as supplied by Wikidata.

Film metadata, Rotten Tomatoes and Metacritic scores, review counts, reported
box-office receipts, and recorded Academy Award categories are included where
available. ``BoxOffice`` is the maximum reported US-dollar gross per film,
often worldwide rather than domestic. Award counts can be incomplete.
``Fresh`` and ``Rotten`` are approximate counts derived from the rounded
Tomatometer percentage and review count.

The full legacy ``omdb`` and ``tomatoes`` table schemas are retained for
compatibility with published Bokeh examples. Unavailable values, including
IMDb ratings and votes, user scores, and editorial review text, are ``NULL``.
Missing genre, director, and cast fields are empty strings so existing text
filters work. No synthetic metrics are included.

Source, snapshot, and transformation details are recorded in
``licenses/datasets.json``.

This module has an attribute ``movie_path``. This attribute contains the path
to a SQLite database with the data.

.. bokeh-sampledata-xref:: movies_data

.. _CC0: https://creativecommons.org/publicdomain/zero/1.0/
.. _Wikidata: https://www.wikidata.org/wiki/Wikidata:Copyright

"""

from __future__ import annotations

from . import package_path

__all__ = ("movie_path",)

movie_path = package_path("movies.db")
