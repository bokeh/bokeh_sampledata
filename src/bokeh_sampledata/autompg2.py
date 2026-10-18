# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""EPA fuel economy data for 1999 and 2008 vehicle models.

License: `Public Domain`_

Original source: `FuelEconomy.gov <https://www.fueleconomy.gov/>`_,
provided by the US Department of Energy and Environmental Protection Agency.
This sample contains public-domain EPA vehicle fuel economy records.
The subset was distributed as ggplot2's ``mpg`` dataset.
This is a different dataset from :ref:`sampledata_autompg`.

This module contains one pandas Dataframe: ``autompg2``.

.. rubric:: ``autompg2``

:bokeh-dataframe:`bokeh.sampledata.autompg2.autompg2`

.. bokeh-sampledata-xref:: autompg2

"""

from __future__ import annotations

from . import package_csv

__all__ = ("autompg2",)


def _capitalize_words(string: str) -> str:
    return " ".join(word.capitalize() for word in string.split(" "))


autompg2 = package_csv("auto-mpg2.csv")
autompg2["manufacturer"] = autompg2["manufacturer"].map(_capitalize_words)
autompg2["model"] = autompg2["model"].map(_capitalize_words)
autompg2["drv"] = autompg2["drv"].replace({"f": "front", "r": "rear", "4": "4x4"})
