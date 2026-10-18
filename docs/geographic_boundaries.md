# Geographic boundary records

Shapely is included as a standard dependency of `bokeh_sampledata`:

```python
from bokeh_sampledata import us_states, us_counties, world_countries

states = us_states.records()
texas = us_counties.records(state="TX")
countries = world_countries.records()
geometry = texas[0]["geometry"]  # Shapely Polygon or MultiPolygon
```

These functions return lists of fresh dictionaries in stable identifier order.
Coordinates are longitude, latitude in degrees, with polygon parts and
interior rings preserved. US coordinates retain the Census NAD83 source;
Natural Earth coordinates are WGS84. No reprojection is applied. All packaged geometries are nonempty and valid.
The APIs do not depend on the packaged storage format.

| Module | Count | Metadata beside `geometry` |
| --- | ---: | --- |
| `us_states` | 51 | `code`, `name`, `region` |
| `us_counties` | 3,233 | `fips`, `state_fips`, `county_fips`, `state`, `name`, `detailed_name` |
| `world_countries` | 242 | `id`, `name`, `iso_a2`, `iso_a3`, `continent`, `region` |

County FIPS identifiers are padded strings: `fips="01001"`,
`state_fips="01"`, `county_fips="001"`. State codes are uppercase postal
abbreviations. The optional `state` argument accepts either case, including
DC and territories, and uses an index before decoding any geometry. Unknown
two-letter ASCII codes return an empty list. Names, numeric FIPS codes,
whitespace, and other formats raise `ValueError`.

Country `id` is Natural Earth's unique `ADM0_A3` identifier. `iso_a2` and
`iso_a3` use its `ISO_A2_EH` and `ISO_A3_EH` fields, with `-99` represented as
`None`. These source codes can be shared by multiple territories and include
unofficial codes such as `XK` for Kosovo; use `id` as the unique key. These
fields provide `FR`, `NO`, and `TW` where the primary source ISO fields have
missing values or an alternative code.

The permanent `us_states.data` and `us_counties.data` compatibility APIs retain
their historical dictionary schemas, NumPy array types, NaN separators, and
metadata interfaces. Coordinates come from the shared valid geometries, so
repairs, ring ordering, and closing points can differ from the old arrays.
They are loaded and cached on first attribute access (including
`from ... import data`). Their reconstruction uses NumPy and the standard
library, with a cache independent of `records()`. Importing these modules
performs no boundary I/O. Both APIs share the packaged WKB with no duplicate
boundary dataset. The old KML-in-CSV files are no longer included in the
package. No GeoPandas or PyArrow dependency is required.

## Boundary data provenance

US geometry is derived directly from the repository's historical
`US_Regions_State_Boundaries.csv.gz` and `US_Counties.csv` at revision `4195d5e`,
not from a new or current census release. Coordinate comparison identifies
simplified Census TIGER/Line geometry: all state vertices and over 99.99% of
county vertices match the official 2009 release at the source rounding
precision. The exact acquisition vintage and export intermediary remain
unrecorded; these are historical samples, not current administrative geography. Existing
metadata (including source character replacement artifacts) is retained.
Sixteen duplicate Puerto Rico FIPS rows use the last source row, matching the
legacy dictionary. Unlike the historical plotting arrays, records also read
interior rings and rings without a `LinearRing` wrapper.

Generation repairs invalid geometry using Shapely `make_valid`; polygonal
components are retained and collapsed line/point remnants discarded. This
repairs Alaska and 45 counties; the exact identifiers are recorded in the
packaged `geographic_boundaries.json` manifest. No world-country repairs were
needed. The legacy dictionary schemas, NumPy array types, NaN separators, and source
iteration order are retained. Lazy legacy access extracts exterior coordinates
from the same WKB with a small standard-library decoder. Interior holes remain
available in `records()` but are omitted from the historical `lats`/`lons`
interface. Coordinate values can differ due to repairs and polygon closing;
exact historical arrays are not a compatibility guarantee. The original source
files are fetched only for regeneration from a pinned historical revision.

World geometry comes from [Natural Earth Admin 0 countries, 1:50m, version
5.1.1](https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/).
It includes countries and territories and follows **de facto control**, not
necessarily legal sovereignty or any particular government's boundary claims.
See Natural Earth's [disputed boundaries policy](https://www.naturalearthdata.com/about/disputed-boundaries-policy/).
Natural Earth data is [public domain](https://www.naturalearthdata.com/about/terms-of-use/),
including commercial use and redistribution; attribution is not required.
These terms are compatible with distributing the dataset alongside BSD-3-Clause
software; the Natural Earth data itself remains public domain.

The installed package includes a [boundary provenance and license notice](../src/bokeh_sampledata/_data/geographic_boundaries.LICENSE.txt),
which records the US source evidence and remaining uncertainties. The US
geometry matches [Census TIGER/Line sources](https://www2.census.gov/geo/tiger/TIGER2009/).
Their embedded metadata declares the shapefiles not copyrighted and permits
use in products/publications with Census acknowledgement. The notice includes
that credit; these terms are compatible with BSD redistribution.

Storage and reproducible regeneration are described in
[tools/README.md](../tools/README.md). The manifest records source checksums,
counts, repairs, tool versions, and database checksum and size.
