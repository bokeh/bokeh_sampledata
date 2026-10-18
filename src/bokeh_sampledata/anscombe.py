# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""The four data series that comprise `Anscombe's Quartet`_.

License: `Public Domain`_

Francis J. Anscombe (1973), “Graphs in Statistical Analysis”,
The American Statistician, 27(1), 17-21, https://doi.org/10.1080/00031305.1973.10478966.
The historical scientific data values are public domain.

This module contains one pandas Dataframe: ``data``.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.anscombe.data`

.. bokeh-sampledata-xref:: anscombe

.. _Anscombe's Quartet: https://en.wikipedia.org/wiki/Anscombe%27s_quartet

"""

from __future__ import annotations

from . import package_csv

__all__ = ("data",)

data = package_csv("anscombe.csv", skipinitialspace=True)
