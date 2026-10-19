# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Provides access to ``probly.csv`` and ``numberly.csv``.

License: `MIT license`_. Copyright (c) 2016 Zoni Nation.
The original notice ships in ``licenses/MIT.txt``.
Survey responses were collected through Reddit's r/SampleSize community.

Sourced from: https://github.com/zonination/perceptions

This module contains two pandas Dataframes: ``probly`` and ``numberly``.

.. rubric:: ``probly``

:bokeh-dataframe:`bokeh.sampledata.perceptions.probly`

.. rubric:: ``numberly``

:bokeh-dataframe:`bokeh.sampledata.perceptions.numberly`

.. bokeh-sampledata-xref:: perceptions

"""

from __future__ import annotations

from . import package_csv

__all__ = ("numberly", "probly")

numberly = package_csv("numberly.csv")
probly = package_csv("probly.csv")
