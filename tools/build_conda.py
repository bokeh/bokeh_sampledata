# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Build and test a local noarch package from a freshly built wheel using rattler."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import zipfile
from email.parser import Parser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="conda-wheel-", dir=work) as temporary:
        subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", temporary], cwd=ROOT, check=True
        )
        (wheel,) = Path(temporary).glob("*.whl")
        with zipfile.ZipFile(wheel) as archive:
            (metadata,) = (name for name in archive.namelist() if name.endswith(".dist-info/METADATA"))
            version = Parser().parsestr(archive.read(metadata).decode())["Version"]
        subprocess.run(
            [
                "rattler-build",
                "build",
                "--recipe",
                str(ROOT / "conda"),
                "--channel",
                "conda-forge",
                "--output-dir",
                str(ROOT / "dist/conda"),
            ],
            cwd=ROOT,
            check=True,
            env={**os.environ, "VERSION": version, "WHEEL_PATH": str(wheel)},
        )


if __name__ == "__main__":
    main()
