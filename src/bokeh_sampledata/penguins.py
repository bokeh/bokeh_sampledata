# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Provide data from the `Palmer Archipelago (Antarctica) penguin dataset`_.

License: `CC0`_, as stated by the original palmerpenguins project.
Data were collected and made available by Kristen Gorman and Palmer Station,
Antarctica LTER. The simplified data is distributed via seaborn-data.
Palmerpenguins: Allison Horst, Alison Hill and Kristen Gorman (2020),
`DOI: 10.5281/zenodo.3960218 <https://doi.org/10.5281/zenodo.3960218>`_.

Sourced from https://github.com/mwaskom/seaborn-data/blob/master/penguins.csv

This module contains one pandas Dataframe: ``data``.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.penguins.data`

.. bokeh-sampledata-xref:: penguins

.. _Palmer Archipelago (Antarctica) penguin dataset: https://github.com/allisonhorst/palmerpenguins

"""

from __future__ import annotations

from . import package_csv

__all__ = ("data",)

data = package_csv("penguins.csv")
