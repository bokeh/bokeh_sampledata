# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""A table of `Will Burtin's historical data`_ regarding antibiotic
efficacies.

License: `MIT license`_

Sourced from: https://gist.github.com/borgar/cd32f1d804951034b224

This module contains one pandas Dataframe: ``data``.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.antibiotics.data`

.. bokeh-sampledata-xref:: antibiotics

.. _Will Burtin's historical data: https://gist.github.com/borgar/cd32f1d804951034b224

"""

from __future__ import annotations

from . import package_csv

__all__ = ("data",)

data = package_csv("antibiotics.csv", skipinitialspace=True)
