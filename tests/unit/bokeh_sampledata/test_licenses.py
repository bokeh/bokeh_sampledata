# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Coverage and integrity of the packaged data's license inventory."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from importlib.metadata import metadata
from pathlib import Path

from packaging.licenses import canonicalize_license_expression

from bokeh_sampledata import package_dir

ROOT = Path(__file__).resolve().parents[3]


def test_dataset_license_inventory() -> None:
    inventory = json.loads((ROOT / "licenses/datasets.json").read_text(encoding="utf-8"))
    data_dir = package_dir()
    actual = {path.relative_to(data_dir).as_posix() for path in data_dir.rglob("*") if path.is_file()}
    listed = [name for entry in inventory["datasets"] for name in entry["files"]]
    assert len(listed) == len(set(listed)), "Each data file must have exactly one license inventory entry"
    assert set(listed) == actual
    for entry in inventory["datasets"]:
        assert entry["status"] in inventory["statuses"]
        assert entry["attribution"] and entry["notes"]
        assert set(entry["sha256"]) == set(entry["files"])
        for name, expected in entry["sha256"].items():
            assert hashlib.sha256((data_dir / name).read_bytes()).hexdigest() == expected, name
        for name, expected in entry.get("uncompressed_sha256", {}).items():
            assert name in entry["files"]
            with gzip.GzipFile(data_dir / name, "rb") as stream:
                assert hashlib.sha256(stream.read()).hexdigest() == expected, name


def test_retrieved_license_texts_are_unmodified() -> None:
    directory = ROOT / "licenses"
    sources = json.loads((directory / "text-sources.json").read_text(encoding="utf-8"))
    for name, source in sources.items():
        assert source["source"].startswith("https://")
        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == source["sha256"], name


def test_dataset_license_expressions_and_notices() -> None:
    expression = metadata("bokeh_sampledata")["License-Expression"]
    assert expression == "BSD-3-Clause"
    inventory = json.loads((ROOT / "licenses/datasets.json").read_text(encoding="utf-8"))
    for entry in inventory["datasets"]:
        license_expression = entry["license_expression"]
        if license_expression is None:
            assert "public domain" in entry["recorded_license"].lower()
        else:
            assert canonicalize_license_expression(license_expression)
    for entry in inventory["datasets"]:
        for identifier in re.findall(r"LicenseRef-[A-Za-z0-9.-]+", entry["license_expression"] or ""):
            assert (ROOT / "licenses" / f"{identifier}.txt").is_file() or (
                entry.get("license_text") and entry["sources"]
            ), identifier
