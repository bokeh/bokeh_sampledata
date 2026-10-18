# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Character encounters in Les Misérables, from Donald Knuth's Stanford GraphBase.

Derived from ``jean.dat``, Copyright 1993 Stanford University. This renamed JSON
file is not part of the Stanford GraphBase. Knuth describes its programs and
data as public domain. Its accompanying file notice permits redistribution
and requires renamed, identified derivatives. See ``licenses/LicenseRef-Stanford-GraphBase.txt``.

The 77 characters and 254 weighted links retain the historical Bokeh graph.
Groups are independently computed by deterministic Louvain community detection,
rather than copied from Mike Bostock's visualization. They are illustrative
clusters, not additional literary facts.

Source: https://www-cs-faculty.stanford.edu/~knuth/sgb.html

This module contains one dictionary, ``data``, with ``nodes`` (name and group)
and ``links`` (integer source and target node indices, and encounter count value).

.. bokeh-sampledata-xref:: les_mis

"""

from __future__ import annotations

import json

from . import package_path

__all__ = ("data",)

with open(package_path("les_mis.json"), "rb") as f:
    data = json.load(f)
