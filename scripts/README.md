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

Run from the repository root, keeping downloads and the environment in `work/`:

```sh
python3 -m venv work/venv
work/venv/bin/python -m pip install 'shapely==2.1.2' 'pyshp==2.3.1'
mkdir -p work/boundary-sources
curl -L --fail https://raw.githubusercontent.com/bokeh/bokeh_sampledata/4195d5e5c3094ef578be168778c7e9501138f921/src/bokeh_sampledata/_data/US_Counties.csv \
  -o work/boundary-sources/US_Counties.csv
curl -L --fail https://raw.githubusercontent.com/bokeh/bokeh_sampledata/4195d5e5c3094ef578be168778c7e9501138f921/src/bokeh_sampledata/_data/US_Regions_State_Boundaries.csv.gz \
  -o work/boundary-sources/US_Regions_State_Boundaries.csv.gz
curl -L --fail https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip \
  -o work/ne_50m_admin_0_countries.zip
work/venv/bin/python scripts/generate_boundaries.py work/ne_50m_admin_0_countries.zip
```

The script rejects any archive whose SHA-256 differs from
`5fed433373581fa648920435f937d95f2d3c0200e067409c6478dcdf1b853139`, and
verifies its version file is 5.1.1. The two US inputs must be fetched from the pinned repository revision above.
Their SHA-256 hashes are checked before conversion.
No boundary downloads occur during generation, installation, or runtime.
PyShp is a generation-only dependency, not a runtime requirement.

Sorted insertion, fixed byte order, fixed compression level, and a fresh
vacuumed database produce byte-identical output with the same toolchain.
The initial generation used CPython 3.14.6, SQLite 3.53.1, zlib 1.2.12,
Shapely 2.1.2 / GEOS 3.13.1 and PyShp 2.3.1. Different SQLite, zlib, or GEOS
versions can change binary bytes; use the recorded versions for exact
checksums and review/rebaseline the manifest deliberately on upgrades.
The script accepts `--source-dir` to select the US input directory and `--output work/geographic_boundaries.db` for comparison
without replacing the packaged artifact. The source archives and CSV inputs remain outside the package. Commit both the database and its
JSON manifest after regeneration, never the source archive or environment.

To run the regeneration test as well as runtime tests:

```sh
work/venv/bin/python -m pip install -e '.[geometry]' pytest
NATURAL_EARTH_ARCHIVE=work/ne_50m_admin_0_countries.zip \
  work/venv/bin/python -m pytest tests/unit/bokeh_sampledata/test_boundaries.py
```

Without that environment variable, the regeneration test skips; other tests
require no archive or PyShp. The test regenerates twice and compares the bytes
to each other and the checked-in database. Run it with the recorded generation
toolchain. CI installs the geometry extra to exercise the runtime API on all
supported CI platforms. Legacy imports/access are also tested in fresh
subprocesses where Shapely is unavailable.
