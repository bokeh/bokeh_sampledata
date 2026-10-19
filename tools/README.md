# Regenerating geographic boundaries

The database uses standard-library SQLite, as does the existing `movies.db`
sample. Each table contains a stable identifier, indexed state code where
applicable, JSON metadata, and **little-endian 2D WKB** per row.
Each row also retains its original iteration ordinal. US legacy dictionaries
are built lazily from shared WKB exteriors using Shapely.
No duplicate coordinate payload or original CSV is packaged.
The historical plotting schemas are preserved, while coordinates may differ
due to repairs or polygon closing.
A county state index allows filtered reads without loading all county geometries.
WKB is stored without per-row compression so wheel ZIP compression can exploit
repeated coordinates across records. Runtime requires only Shapely
and the standard library, alongside the package's existing dependencies.
The public records API is independent of these implementation choices.

Run from the repository root. Downloads stay in ignored `work/`. Pixi manages
the environment under `.pixi/`:

```sh
pixi run --locked setup
mkdir -p work/boundary-sources
curl -L --fail https://raw.githubusercontent.com/bokeh/bokeh_sampledata/4195d5e5c3094ef578be168778c7e9501138f921/src/bokeh_sampledata/_data/US_Counties.csv \
  -o work/boundary-sources/US_Counties.csv
curl -L --fail https://raw.githubusercontent.com/bokeh/bokeh_sampledata/4195d5e5c3094ef578be168778c7e9501138f921/src/bokeh_sampledata/_data/US_Regions_State_Boundaries.csv.gz \
  -o work/boundary-sources/US_Regions_State_Boundaries.csv.gz
curl -L --fail https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip \
  -o work/ne_50m_admin_0_countries.zip
pixi run --locked regenerate-boundaries
```

The script rejects any archive whose SHA-256 differs from
`5fed433373581fa648920435f937d95f2d3c0200e067409c6478dcdf1b853139`, and
verifies its version file is 5.1.1. The two US inputs must be fetched from the pinned repository revision above.
Their SHA-256 hashes are checked before conversion.
No boundary downloads occur during generation, installation, or runtime.
PyShp is a generation-only dependency, not a runtime requirement.

Sorted insertion, fixed byte order, and a fresh
vacuumed database produce byte-identical output with the same toolchain.
The checked-in generation used the locked default Pixi environment on macOS
Apple Silicon: CPython 3.12.15, SQLite 3.54.1, Shapely 2.2.0 /
GEOS 3.14.1 and PyShp 2.3.1. Different SQLite or GEOS
versions can change binary bytes. Use the recorded versions for exact
checksums and review/rebaseline the manifest deliberately on upgrades.
The script accepts `--source-dir` to select the US input directory and `--output work/geographic_boundaries.db` for comparison
without replacing the packaged artifact. The source archives and CSV inputs remain outside the package. Commit both the database and its
JSON manifest after regeneration, never the source archive or environment.

To run the regeneration test as well as runtime tests:

```sh
pixi run --locked test-regeneration
```

The task sets `NATURAL_EARTH_ARCHIVE` to the downloaded archive. Without that
environment variable, the regeneration test skips. Other tests
require no archive or PyShp. The test regenerates twice and compares the bytes
to each other and the checked-in database. Run it with the recorded generation
toolchain. CI includes Shapely in its locked test environments to exercise the runtime API on all
supported CI platforms. Lazy legacy imports and attribute caching are also
tested in fresh subprocesses.

## Historical stock data

The combined `stocks.csv.gz` contains extracts of Quandl WIKI Prices from the archived
copy linked in the stocks module docstring. The source archive and CSV hashes
are recorded in `licenses/datasets.json`. Select the original date ranges
through March 1, 2013, keep raw OHLCV and adjusted close, convert volume to
integer, and sort each ticker's rows by date. Add a ticker column to identify
each series. Use the source's `GOOGL` history for the legacy
`GOOG` API. Gzip headers omit filenames and timestamps for reproducible output.

## Browser icons

The five SVG outlines come from Font Awesome Free tag `6.7.2`, under
`svgs/brands/`: `chrome.svg`, `firefox.svg`, `internet-explorer.svg`, `opera.svg`,
and `safari.svg`. Pinned source URLs and SHA-256 hashes are recorded in
`licenses/datasets.json`.

The PNGs were rendered with `@resvg/resvg-js` 2.6.2. Preserve each original path,
scale it uniformly to fit a 28-by-28 area, and center it in a transparent
32-by-32 canvas. Fill colors are Chrome `#4285f4`, Firefox `#e66000`, Internet
Explorer `#0078d7`, Opera `#d80a1f`, and Safari `#007aff`. PNG `tEXt` metadata
records Fonticons attribution, CC BY 4.0, the exact SVG URL and the changes.
Retain those notices, `licenses/Font-Awesome.txt`, and the source hashes when
replacing assets. Rendering is a one-off development step with no added runtime
dependency. No Font Awesome font or JavaScript code is distributed.

## Packaged text compression

Larger CSV/JSON datasets and the consolidated stock and Gapminder tables are
stored as gzip. Small
files, the boundary manifest, and formats consumed by external tools remain
unchanged. Pandas infers gzip from the filename, while dictionary loaders open
gzip streams directly. No extraction cache or additional dependency is needed.

Preserve the original bytes when compressing data. Use level 9, an empty gzip
filename, and timestamp zero. The inventory records both the packaged hash and
the uncompressed content hash so a storage change does not obscure provenance.
