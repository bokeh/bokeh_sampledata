# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Automobile data from the 1983 ASA Data Exposition.

License: `CC0`_

Original compilation: David Donoho and Ernesto Ramos (1982),
``PRIMDATA: Data Sets for Use With PRIM-H``, ``CRCARS`` dataset.
The `1983 ASA exposition instructions
<https://lib.stat.cmu.edu/datasets/cars.desc>`_ identify this source.

This sample contains the 392 complete records from the 406-car dataset
archived by `StatLib <https://lib.stat.cmu.edu/datasets/cars.data>`_, with
renamed columns. Both numeric values and car names retain the original order.

This module contains two pandas Dataframes: ``autompg`` and ``autompg_clean``.
The "clean" version has cleaned up the ``"mfr"`` and ``"origin"`` fields.

.. rubric:: ``autompg``

:bokeh-dataframe:`bokeh.sampledata.autompg.autompg`

.. rubric:: ``autompg_clean``

:bokeh-dataframe:`bokeh.sampledata.autompg.autompg_clean`

.. bokeh-sampledata-xref:: autompg

"""

from __future__ import annotations

import pandas as pd

from . import package_csv

__all__ = ("autompg", "autompg_clean")


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["mfr"] = [x.split()[0] for x in df.name]
    df.loc[df.mfr == "chevy", "mfr"] = "chevrolet"
    df.loc[df.mfr == "chevroelt", "mfr"] = "chevrolet"
    df.loc[df.mfr == "maxda", "mfr"] = "mazda"
    df.loc[df.mfr == "mercedes-benz", "mfr"] = "mercedes"
    df.loc[df.mfr == "toyouta", "mfr"] = "toyota"
    df.loc[df.mfr == "vokswagen", "mfr"] = "volkswagen"
    df.loc[df.mfr == "vw", "mfr"] = "volkswagen"

    ORIGINS = {1: "North America", 2: "Europe", 3: "Asia"}
    df["origin"] = [ORIGINS[x] for x in df["origin"]]

    return df


autompg = package_csv("auto-mpg.csv")

autompg_clean = _clean_data(autompg)
