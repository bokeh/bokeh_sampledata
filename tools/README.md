# Regenerating geographic boundaries

The database uses standard-library SQLite, as does the existing `movies.db`
sample. Each table contains a stable identifier, indexed state code where
applicable, JSON metadata, and **zlib-compressed little-endian 2D WKB** per row.
Each row also retains its original iteration ordinal. US legacy dictionaries
are built lazily from shared WKB exteriors using a standard-library decoder,
without Shapely. No duplicate coordinate payload or original CSV is packaged.
The historical plotting schemas are preserved, while coordinates may differ
due to repairs or polygon closing.
Per-row compression and a county state index allow filtered reads without
loading or decompressing all county geometries. Runtime requires only Shapely
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

Sorted insertion, fixed byte order, fixed compression level, and a fresh
vacuumed database produce byte-identical output with the same toolchain.
The checked-in generation used the locked default Pixi environment on macOS
Apple Silicon: CPython 3.12.15, SQLite 3.54.1, zlib 1.3.2, Shapely 2.2.0 /
GEOS 3.14.1 and PyShp 2.3.1. Different SQLite, zlib, or GEOS
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
supported CI platforms. Legacy imports/access are also tested in fresh
subprocesses where Shapely is unavailable.
