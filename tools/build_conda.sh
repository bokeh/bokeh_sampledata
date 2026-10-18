#!/usr/bin/env bash
# Copyright (c) Bokeh Contributors. See LICENSE.txt for the full license.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

mkdir -p work
wheel_dir=$(mktemp -d "$PWD/work/conda-wheel.XXXXXX")
trap 'rm -rf "$wheel_dir"' EXIT

python -m build --wheel --no-isolation --outdir "$wheel_dir"
wheels=("$wheel_dir"/bokeh_sampledata-*-py3-none-any.whl)
if [[ ${#wheels[@]} -ne 1 || ! -f ${wheels[0]} ]]; then
    printf 'Expected one bokeh_sampledata wheel\n' >&2
    exit 1
fi

wheel=${wheels[0]}
# The wheel filename encodes the distribution version (PEP 427).
version=${wheel##*/}
version=${version#bokeh_sampledata-}
version=${version%-py3-none-any.whl}

VERSION="$version" WHEEL_PATH="$wheel" rattler-build build \
    --recipe conda --channel conda-forge --output-dir dist/conda
