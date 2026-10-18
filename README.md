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
and build tools. `test-py310`, `test-py311`, `test-py312`, `test-py313`,
`test-py314`, and `test-py315` provide explicit test environments.
`test-py310-minimum` pins NumPy 1.26.4 and pandas 2.2.3 to verify the declared runtime floors on Python
3.10. For example:

```sh
pixi run --locked -e test-py310 test
pixi run --locked -e test-py310-minimum test
pixi run --locked -e build build-py
```

`build-py` creates a wheel and sdist in `dist/` using the isolated `build`
environment. It does not publish packages. Conda-forge distribution is handled
downstream, with no conda packaging recipe maintained in this repository.

Boundary storage and regeneration instructions are in [tools/README.md](tools/README.md).
User-facing API, compatibility, and provenance documentation lives in the public
module/function docstrings, which are included in the main Bokeh documentation.

CI runs locked test environments on Linux, macOS, and Windows for Python
3.10–3.15, the minimum-dependency environment on Linux, plus repository checks
and package builds on Linux. The package job runs the unit suite against an
installed wheel in a separate environment. To reproduce that check after
`build-py`, run `pixi run --locked -e wheel-test test-wheel`.

Python 3.10 remains the package minimum. NumPy is declared directly because the
package uses its arrays. Runtime requirements are mirrored in the Pixi manifest,
including Shapely as a standard runtime dependency.

`pixi run --locked dependency-check` checks that runtime requirements agree
between the Python metadata and Pixi manifest. Ruff handles both linting and
import sorting.

`check` also runs actionlint on GitHub Actions workflows. The same check runs
from pre-commit when a workflow changes. Hooks check for merge conflict markers,
case-conflicting filenames, broken symlinks, private keys, and large additions
outside the dataset directory, alongside formatting.
Install the hooks locally with `pixi run --locked pre-commit install`.
Hooks use isolated pre-commit environments and also run on pre-commit.ci without
Pixi. Hook revisions are pinned to commit hashes and local hook tools use exact
versions. Update remote hooks with `pre-commit autoupdate --freeze`.

Type checking uses both Mypy (strict mode) and Pyright (standard mode), targeting
Python 3.10 across `src`, `tests`, and `tools`. Run both with
`pixi run --locked typecheck`, or individually with `typecheck-mypy` and
`typecheck-pyright`. Both also run through `check` and the CI quality job, using
the locked Pixi environment rather than pre-commit environments.

## Releases

Publishing a GitHub release runs `.github/workflows/release.yml`. The workflow
checks out the release tag, builds the sdist and a wheel from that sdist,
checks that their versions match the tag, and tests the installed wheel.
A separate job publishes those same distributions to PyPI using trusted
publishing through the `pypi` GitHub environment. No PyPI API token is needed.
Tags follow the existing version format, for example `2025.0`.

The environment approval is the final step before uploading the tested artifacts.

## License maintenance

The software license is in [LICENSE.txt](LICENSE.txt). Dataset notices and
provenance are collected in [licenses/](licenses/README.md).
Update [the file inventory](licenses/datasets.json) when adding or replacing data,
including original source evidence, attribution, applicable terms, and changes
made to the source. Keep legal texts verbatim. Existing license declarations are accepted unless contrary evidence is found.
Record explicit terms for new datasets before including them.
