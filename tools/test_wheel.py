# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Install the built wheel and run unit tests in the dedicated wheel-test environment."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    wheels = list((ROOT / "dist").glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError("Expected exactly one wheel in dist/. Run build-py with a clean dist/ directory.")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-deps", "--force-reinstall", str(wheels[0])], check=True
    )
    # Isolated mode ignores PYTHONPATH and the working directory. Verify the
    # import resolves inside this environment before collecting the unit suite.
    subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            """
import sys
from pathlib import Path
import bokeh_sampledata
path = Path(bokeh_sampledata.__file__).resolve()
assert path.is_relative_to(Path(sys.prefix).resolve()), path
print(f'Testing installed package: {path}')
""",
        ],
        check=True,
    )
    subprocess.run(
        [sys.executable, "-I", "-m", "pytest", "--import-mode=importlib", str(ROOT / "tests/unit")],
        check=True,
        cwd=ROOT,
    )


if __name__ == "__main__":
    main()
