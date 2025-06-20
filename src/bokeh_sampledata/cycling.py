# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Exercise data (including altitude, speed and power) from a cycling workout.

This module contains one pandas Dataframe: ``cycling``.

.. rubric:: ``cycling``

:bokeh-dataframe:`bokeh.sampledata.cycling.cycling`

.. bokeh-sampledata-xref:: cycling

"""

from __future__ import annotations

import pandas as pd

from . import package_csv

__all__ = ("cycling",)


def _read_data() -> pd.DataFrame:
    df = package_csv("cycling.csv")
    df["time"] = pd.to_timedelta(df["time"])
    return df


cycling = _read_data()
