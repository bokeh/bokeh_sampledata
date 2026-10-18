# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Check runtime requirements across Python and Pixi metadata."""

from __future__ import annotations

import sys
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]


def requirements(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        requirement = Requirement(value)
        if requirement.extras or requirement.marker or requirement.url:
            raise ValueError(f"Cannot mirror conditional or direct requirement: {value}")
        result[canonicalize_name(requirement.name)] = str(requirement.specifier)
    return result


def main() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    pixi = tomllib.loads((ROOT / "pixi.toml").read_text())
    expected = requirements(project["project"]["dependencies"])
    # These base Pixi dependencies support editable installation and builds.
    build_tools = {"pip", "setuptools", "setuptools-git-versioning", "wheel"}
    pixi_runtime = requirements(
        [
            f"{name}{version if version != '*' else ''}"
            for name, version in pixi["dependencies"].items()
            if name not in build_tools
        ]
    )
    if pixi_runtime != expected:
        raise ValueError(f"pixi.toml runtime requirements {pixi_runtime} differ from pyproject.toml {expected}")
    print("Python and Pixi runtime requirements agree")


if __name__ == "__main__":
    main()
