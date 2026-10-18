# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""The ``bokeh.sampledata`` module can be used to access data sets used in
Bokeh examples.

In order to access these data sets, the separate ``bokeh_sampledata`` package
must be pip or conda installed.

Bokeh's loader code is BSD-3-Clause. Bundled datasets and browser logos retain
separate terms. Source credits, legal texts, and dataset license declarations
are documented in the distribution's license files, especially
``licenses/datasets.json``. Installed wheels place these under the package's
``.dist-info/licenses/`` directory. Module documentation gives the relevant per-dataset notice.
No single BSD grant covers all bundled data.

"""

from __future__ import annotations

import importlib.metadata as importlib_metadata
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

__all__ = ("__version__",)


__version__ = importlib_metadata.version("bokeh_sampledata")


def package_csv(name: str, **kw: Any) -> pd.DataFrame:
    import pandas as pd

    return pd.read_csv(package_path(name), **kw)


def package_dir() -> Path:
    return Path(__file__).parent.joinpath("_data").resolve()


def package_path(filename: str | Path) -> Path:
    return package_dir() / filename
