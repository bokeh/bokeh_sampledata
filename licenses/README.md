# Software and dataset licenses

Bokeh's Python code, tests, tools, original documentation, and original
illustrative data use BSD-3-Clause, reproduced in the top-level
[LICENSE.txt](../LICENSE.txt). Other datasets retain their own terms.

[datasets.json](datasets.json) records source links, attribution, applicable
license expressions, transformations, and packaged SHA-256 hashes. Gzip entries
also record uncompressed content hashes. Public-domain status is stated directly,
without an invented SPDX identifier. Entries with no files describe calculated
module data. Historical `replaces` records do not contribute terms to the current
package. Existing declarations are retained unless contrary evidence was found.

## Included notices and attribution

- Statcounter browser statistics retain CC-BY-SA-3.0 and source credit.
- Browser icons use Font Awesome Free 6.7.2 under CC BY 4.0. PNG metadata records
  Fonticons attribution and the rasterization/color/padding changes.
  The upstream notice is in `Font-Awesome.txt`.
- GeoNames cities use acquisition-era CC BY 3.0. Gapminder retains its historical
  CC BY 2.0 declaration. Other CC BY datasets retain their recorded source credits.
- Perceptions retains the upstream MIT notice in `MIT.txt`.
- The original Haar classifier retains its file-specific Intel OpenCV BSD-style
  notice in the XML and `LicenseRef-Intel-OpenCV.txt`. Redistribution is permitted
  with that notice retained. The compact package expression remains BSD-3-Clause.
- Les Misérables nodes and encounter links derive from Knuth's `jean.dat`.
  The renamed JSON is not part of the Stanford GraphBase. Its source notice is
  in `LicenseRef-Stanford-GraphBase.txt`. Community groups are independently
  calculated, avoiding reliance on an unverified early Bostock license.
- Historical NHS area-team GeoJSON retains the Open Government Licence v2.0
  attribution. The full text is in `OGL-UK-2.0.txt`.
- Population uses United Nations World Population Prospects 2024 under
  CC BY 3.0 IGO, with UN credit and the subset/reshaping/unit conversion described
  in the module and inventory. Its license is in `CC-BY-3.0-IGO.txt`.
- Airport locations use public-domain OurAirports records. The real route network
  derives from July 2026 U.S. DOT/BTS flight reports, with source credit retained.
- NERACOOS permission and disclaimer wording is recorded directly in the inventory.
- Census boundary terms and provenance are in
  [geographic-boundaries.txt](geographic-boundaries.txt).
- Original historical Bokeh contributions use the top-level BSD notice, as
  confirmed by the maintainer. The glucose and Anscombe public-domain statements
  retain the maintainer's confirmations.

Third-party notice wording is preserved verbatim.
[text-sources.json](text-sources.json) records source URLs and hashes for
retrieved legal texts. The top-level license and this directory ship in both
sdist and wheel, under `.dist-info/licenses/` in an installed wheel.

## Distribution metadata

The distribution metadata identifies the software license as BSD-3-Clause.
Detailed dataset terms remain in the inventory and notices. This does not
relicense those datasets or remove their attribution requirements.

## Replacement datasets

Stock OHLCV values come from Quandl WIKI's public-domain historical data,
with source credit and the archived publisher notice recorded in the inventory.
Movie information comes from CC0 Wikidata structured data. The full legacy SQL
schema is retained, with unavailable fields left empty. No synthetic movie
metrics or editorial review text are included. Source and transformation notes are recorded in `datasets.json`.

The holiday calendar is independently generated from observed federal and
selected cultural/Easter rules. Daylight values are calculated by the BSD module
using NOAA Solar Calculator equations. No daylight CSV is packaged. The original
published Warsaw CSV is recorded in the replacement history.

The original WPP 2012 acquisition-era notice differs from Bokeh's later CC label.
WPP 2024 supplies an explicit redistributable grant and restores historical years,
UN location identifiers, and geographic coverage. The original OpenFlights extract
is not used. BTS supplies observed routes with its source attribution.
