# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Provide the Sample Superstore data set.

License: `CC0`_

Historical Bokeh extract of the Sample Superstore demonstration dataset.
Tableau publishes Sample Superstore files at
https://public.tableau.com/app/learn/sample-data.
The precise source of this historical extract is unrecorded. A similarly named
Kaggle upload carries a CC0 label, but byte identity has not been verified.

This module contains one pandas Dataframe: ``data``.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.sample_superstore.data`

.. bokeh-sampledata-xref:: sample_superstore

"""

from __future__ import annotations

from . import package_csv

__all__ = ("data",)

data = package_csv("SampleSuperstore.csv.gz")
