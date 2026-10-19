# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Fertility, life expectancy, population, and region information from Gapminder.

License: `CC BY 2.0`_

Credit Gapminder.org and the original indicator providers where identified by
Gapminder. These extracts restrict and align the original countries and years.

Sourced from https://www.gapminder.org/data/

The ``data`` DataFrame has one row per country and year, covering 244 countries
from 1964 through 2013. Its columns are ``country``, ``year``, ``fertility``,
``life_expectancy``, ``population``, ``region``, and ``country_id``. Fertility
is children per woman, life expectancy is years, and population is persons.
Missing source values remain missing. Region and identifier fields come from
the historical Gapminder region table.

For example, select a year with ``data[data["year"] == 2010]`` or a country
with ``data[data["country"] == "United States"]``.

.. rubric:: ``data``

:bokeh-dataframe:`bokeh.sampledata.gapminder.data`

The module also provides the country-by-year DataFrames ``fertility``,
``life_expectancy``, and ``population``, with string year columns, and the
country-indexed ``regions`` metadata table.

.. rubric:: ``fertility``

:bokeh-dataframe:`bokeh.sampledata.gapminder.fertility`

.. rubric:: ``life_expectancy``

:bokeh-dataframe:`bokeh.sampledata.gapminder.life_expectancy`

.. rubric:: ``population``

:bokeh-dataframe:`bokeh.sampledata.gapminder.population`

.. rubric:: ``regions``

:bokeh-dataframe:`bokeh.sampledata.gapminder.regions`

.. bokeh-sampledata-xref:: gapminder

"""

from __future__ import annotations

import pandas as pd

from . import package_csv

__all__ = ("data", "fertility", "life_expectancy", "population", "regions")

_INDICATORS = ("fertility", "life_expectancy", "population")


def _read_data() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    # Read original numeric spellings so each legacy year column retains its dtype.
    rows = package_csv("gapminder.csv.gz", dtype=dict.fromkeys(_INDICATORS, str))
    tables = {}
    for indicator in _INDICATORS:
        table = rows.pivot(index="country", columns="year", values=indicator)
        table = table.reindex(rows["country"].drop_duplicates())
        table = table.apply(pd.to_numeric)
        table.index.name = "Country"
        table.columns = table.columns.astype(str)
        table.columns.name = None
        tables[indicator] = table
        rows[indicator] = pd.to_numeric(rows[indicator])
    return rows, tables


regions = package_csv("gapminder_regions.csv", index_col="Country", encoding="utf-8")
data, _tables = _read_data()
data = data.join(regions.rename(columns={"Group": "region", "ID": "country_id"}), on="country", validate="many_to_one")
fertility = _tables["fertility"]
life_expectancy = _tables["life_expectancy"]
population = _tables["population"]
del _tables

# Original data is from Gapminder - www.gapminder.org.
# These original spreadsheet URLs are historical identifiers. Some no longer
# resolve. Current downloads and documentation are at https://www.gapminder.org/data/
#
# population_url = "http://spreadsheets.google.com/pub?key=phAwcNAVuyj0XOoBL_n5tAQ&output=xls"
# fertility_url = "http://spreadsheets.google.com/pub?key=phAwcNAVuyj0TAlJeCEzcGQ&output=xls"
# life_expectancy_url = "http://spreadsheets.google.com/pub?key=tiAiXcrneZrUnnJ9dBU-PAw&output=xls"
# regions_url = "https://docs.google.com/spreadsheets/d/1OxmGUNWeADbPJkQxVPupSOK5MbAECdqThnvyPrwG5Os/pub?gid=1&output=xls"
