# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Browser market share by version from November 2013.

The statistics are licensed under `CC BY-SA 3.0`_. Credit
`Statcounter Global Stats <https://gs.statcounter.com/>`_ with a link when
reusing them, as requested in https://gs.statcounter.com/faq.
The CSV is a historical extract.

The browser icons are from `Font Awesome Free 6.7.2
<https://github.com/FortAwesome/Font-Awesome/tree/6.7.2/svgs/brands>`_,
Copyright 2024 Fonticons, Inc., under `CC BY 4.0
<https://creativecommons.org/licenses/by/4.0/>`_. Bokeh rasterizes, colors,
and pads the SVG outlines to 32-by-32 PNGs. Attribution and source links are
embedded in each PNG and recorded in ``licenses/datasets.json``.
The upstream notice ships in ``licenses/Font-Awesome.txt``.
Brand icons identify their respective browsers and do not imply endorsement.

This module contains one pandas Dataframe: ``browsers_nov_2013``.

.. rubric:: ``browsers_nov_2013``

:bokeh-dataframe:`bokeh.sampledata.browsers.browsers_nov_2013`

The module also contains a dictionary ``icons`` with 32-by-32 PNG browser icons
for Chrome, Firefox, Safari, Opera, and IE.

.. bokeh-sampledata-xref:: browsers

"""

from __future__ import annotations

from os.path import join

import pandas as pd

from . import package_csv, package_path

__all__ = ("browsers_nov_2013", "icons")


def _read_data() -> pd.DataFrame:
    df = package_csv("browsers_nov_2013.csv", names=("Version", "Share"), skiprows=1)
    versions = df["Version"].str.rsplit(" ", n=1, expand=True)
    df["Browser"] = versions[0]
    df["VersionNumber"] = versions[1].fillna("0")
    return df


def _read_icons() -> dict[str, bytes]:
    icons = {}
    for browser in ("Chrome", "Firefox", "Safari", "Opera", "IE"):
        icon_path = join("icons", f"{browser.lower()}_32x32.png")
        with open(package_path(icon_path), "rb") as icon:
            icons[browser] = icon.read()
    return icons


browsers_nov_2013 = _read_data()
icons = _read_icons()
