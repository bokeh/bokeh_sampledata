# bokeh_sampledata

This package contains sample datasets for use with Bokeh examples.

## Development and packaging

Use [Pixi](https://pixi.sh) >=0.76.1 from the repository root. Commit `pixi.toml`
and `pixi.lock` together when changing dependencies. Environments are locked for
Linux x86-64, macOS Intel/Apple Silicon, and Windows x86-64.

```sh
pixi run --locked setup
pixi run --locked test
pixi run --locked check
pixi run --locked pre-commit run --all-files
```

The default environment uses Python 3.12 and includes geometry, checks, generation,
and build tools. `test-py310`, `test-py311`, `test-py312`, `test-py313`, and
`test-py314` provide explicit test environments; for example:

```sh
pixi run --locked -e test-py310 test
pixi run --locked -e build build-py
pixi run --locked -e build build-conda
```

`build-py` creates a wheel and sdist in `dist/`. `build-conda` builds a fresh
wheel and passes its actual metadata version to **rattler-build**, using
`conda/recipe.yaml`. It creates and tests a noarch package in `dist/conda/`,
including legacy imports and Shapely records. Neither command publishes packages;
no `conda` or `conda-build` command is required. The isolated `build` environment
contains the declared wheel backend and rattler-build.

Boundary storage and regeneration instructions are in [tools/README.md](tools/README.md).
User-facing API, compatibility, and provenance documentation belongs in
[docs/geographic_boundaries.md](docs/geographic_boundaries.md) and the public
module/function docstrings.

CI runs locked test environments on Linux, macOS, and Windows for Python
3.10–3.14, plus repository checks and package builds on Linux. Python 3.10
remains the package minimum. NumPy is declared directly because the package
uses its arrays. Runtime requirements are mirrored in the Pixi manifest and
rattler recipe, including Shapely as a standard runtime dependency.
