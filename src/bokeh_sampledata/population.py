# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Historical and projected population by age, sex, and location.

Source: United Nations, Department of Economic and Social Affairs, Population
Division (2024). World Population Prospects 2024, Online Edition.
https://population.un.org/wpp/

License: `CC BY 3.0 IGO <https://creativecommons.org/licenses/by/3.0/igo/>`_.
Copyright July 2024 United Nations. The sample selects the Medium variant,
five-year intervals from 1950 through 2100, countries and areas, World, regions,
and subregions. Male/female age-group values are reshaped to the legacy columns
and converted from thousands to persons. These changes do not imply UN endorsement.

``LocID`` retains the UN location identifier. Source hashes and transformation
notes are recorded in ``licenses/datasets.json``.

This module contains one pandas DataFrame, ``data``.

:bokeh-dataframe:`bokeh.sampledata.population.data`

.. bokeh-sampledata-xref:: population

"""

from __future__ import annotations

from . import package_csv

__all__ = ("data",)

data = package_csv("population.csv.gz", dtype={"Value": float})
