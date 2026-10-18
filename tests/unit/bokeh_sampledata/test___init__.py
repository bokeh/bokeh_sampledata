# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import subprocess
import sys

import bokeh_sampledata as m


def test_all() -> None:
    assert m.__all__ == ("__version__",)


def test_dictionary_and_text_loaders_do_not_import_pandas() -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            """
import sys
sys.modules['pandas'] = None
import bokeh_sampledata
from bokeh_sampledata import les_mis, sample_geojson, stocks
assert bokeh_sampledata.package_path('AAPL.csv').is_file()
assert stocks.AAPL['date'][0] == '2000-03-01'
assert les_mis.data['nodes']
assert sample_geojson.geojson
""",
        ],
        check=True,
    )
