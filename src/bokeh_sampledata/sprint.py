# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Historical results for Olympic sprints by year.

License: BSD-3-Clause, under the original Bokeh contribution terms.
Source credit: Mateusz Paprocki, Bokeh PR #1484 (2014).
The BSD notice is in the top-level ``LICENSE.txt``.

The original example reproduces the `New York Times 2012 Olympic sprint
visualization <https://archive.nytimes.com/www.nytimes.com/interactive/2012/08/05/sports/olympics/the-100-meter-dash-one-race-every-medalist-ever.html>`_.

This module contains one pandas Dataframe: ``sprint``.

.. rubric:: ``sprint``

:bokeh-dataframe:`bokeh.sampledata.sprint.sprint`

.. bokeh-sampledata-xref:: sprint

"""

from __future__ import annotations

from . import package_csv

__all__ = ("sprint",)

sprint = package_csv(
    "sprint.csv",
    skipinitialspace=True,
    escapechar="\\",
)
