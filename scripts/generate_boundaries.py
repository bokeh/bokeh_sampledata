# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Rebuild geographic_boundaries.db; see scripts/README.md for pinned tooling."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib
from pathlib import Path
from typing import Any

import shapefile
import shapely
from shapely.geometry import (
    GeometryCollection,
    MultiPolygon,
    Polygon,
    shape,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src/bokeh_sampledata/_data"
US_SHA256 = {
    "US_Counties.csv": "db5efb4678f92006ffdf4bad2a1b6decbb4bf0b91ba15dadcc103a2a04718708",
    "US_Regions_State_Boundaries.csv.gz": "6384a4be00b233adee9d30784485f45bc5afb0ad8d01ad874fc4abe5170ee665",
}
ARCHIVE_SHA256 = "5fed433373581fa648920435f937d95f2d3c0200e067409c6478dcdf1b853139"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kml_geometry(text: str) -> Polygon | MultiPolygon:
    root = ET.fromstring(text)
    polygons = [root] if root.tag == "Polygon" else root.findall(".//Polygon")

    def ring(element: ET.Element | None) -> list[tuple[float, ...]]:
        if element is None or element.text is None:
            raise ValueError("Missing polygon ring")
        return [tuple(map(float, coordinate.split(",")[:2])) for coordinate in element.text.split()]

    parts: list[Polygon] = []
    for polygon in polygons:
        outer = polygon.find("outerBoundaryIs/.//coordinates")
        holes = polygon.findall("innerBoundaryIs/.//coordinates")
        parts.append(Polygon(ring(outer), [ring(hole) for hole in holes]))
    return parts[0] if len(parts) == 1 else MultiPolygon(parts)


def generate(archive: Path, output: Path, source_dir: Path) -> dict[str, Any]:
    if digest(archive) != ARCHIVE_SHA256:
        raise ValueError("Natural Earth archive checksum mismatch")
    for name, expected in US_SHA256.items():
        if digest(source_dir / name) != expected:
            raise ValueError(f"US source checksum mismatch: {name}")
    repairs: dict[str, list[str]] = {}
    rows: dict[str, list[tuple[str, str | None, str, bytes]]] = {
        "us_states": [],
        "us_counties": [],
        "world_countries": [],
    }

    def add(
        table: str, identifier: str, state: str | None, metadata: dict[str, Any], geometry: Any, kml: str | None = None
    ) -> None:
        if not geometry.is_valid:
            repairs.setdefault(table, []).append(identifier)
            geometry = shapely.make_valid(geometry)
            if isinstance(geometry, GeometryCollection):
                parts = []
                for part in geometry.geoms:
                    if isinstance(part, Polygon):
                        parts.append(part)
                    elif isinstance(part, MultiPolygon):
                        parts.extend(part.geoms)
                geometry = parts[0] if len(parts) == 1 else MultiPolygon(parts)
        if not isinstance(geometry, Polygon | MultiPolygon) or geometry.is_empty or not geometry.is_valid:
            raise ValueError(f"Invalid polygonal geometry: {table}/{identifier}")
        wkb = shapely.to_wkb(geometry, byte_order=1, output_dimension=2, include_srid=False)
        rows[table].append(
            (
                identifier,
                state,
                json.dumps(metadata, sort_keys=True, ensure_ascii=False),
                zlib.compress(wkb, level=9),
            )
        )

    with gzip.open(source_dir / "US_Regions_State_Boundaries.csv.gz", "rt", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            add(
                "us_states",
                row["id"],
                row["id"],
                dict(code=row["id"], name=row["name"], region=row["Region"]),
                kml_geometry(row["geometry"]),
            )
    with (source_dir / "US_Counties.csv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            state_fips = row["STATE num"].zfill(2)
            county_fips = row["COUNTY num"].zfill(3)
            fips = state_fips + county_fips
            state = row["state abbr"].upper()
            add(
                "us_counties",
                fips,
                state,
                dict(
                    fips=fips,
                    state_fips=state_fips,
                    county_fips=county_fips,
                    state=state,
                    name=row["County Name"],
                    detailed_name=row["Geographic Name"],
                ),
                kml_geometry(row["geometry"]),
            )
    with zipfile.ZipFile(archive) as archive_file:
        stem = "ne_50m_admin_0_countries"
        if archive_file.read(stem + ".VERSION.txt").strip() != b"5.1.1":
            raise ValueError("Unexpected Natural Earth version")
        reader = shapefile.Reader(
            **{ext: io.BytesIO(archive_file.read(f"{stem}.{ext}")) for ext in ("shp", "shx", "dbf")}, encoding="utf-8"
        )
        for feature in reader.iterShapeRecords():
            attributes = feature.record.as_dict()
            metadata = dict(
                id=attributes["ADM0_A3"],
                name=attributes["NAME_EN"],
                iso_a2=None if attributes["ISO_A2_EH"] == "-99" else attributes["ISO_A2_EH"],
                iso_a3=None if attributes["ISO_A3_EH"] == "-99" else attributes["ISO_A3_EH"],
                continent=attributes["CONTINENT"],
                region=attributes["REGION_UN"],
            )
            add("world_countries", metadata["id"], None, metadata, shape(feature.shape.__geo_interface__))
    # Match the historical dictionary's last-row-wins handling of duplicate FIPS.
    for table, records in rows.items():
        rows[table] = list({record[0]: record for record in records}.values())
    output.unlink(missing_ok=True)
    with sqlite3.connect(output) as db:
        db.execute("PRAGMA page_size=4096")
        db.execute("PRAGMA user_version=1")
        for table, records in rows.items():
            db.execute(
                f"CREATE TABLE {table} "
                "(id TEXT PRIMARY KEY, state TEXT, metadata TEXT NOT NULL, "
                "geometry BLOB NOT NULL, ordinal INTEGER NOT NULL)"
            )
            ordered = [(*record, ordinal) for ordinal, record in enumerate(records)]
            db.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?)", sorted(ordered))
        db.execute("CREATE INDEX us_counties_state ON us_counties(state)")
        db.commit()
        db.execute("VACUUM")
    manifest = dict(
        inputs={name: digest(source_dir / name) for name in ("US_Counties.csv", "US_Regions_State_Boundaries.csv.gz")},
        natural_earth_archive_sha256=ARCHIVE_SHA256,
        counts={table: len(records) for table, records in rows.items()},
        repairs=repairs,
        shapely=shapely.__version__,
        geos=shapely.geos_version_string,
        sqlite=sqlite3.sqlite_version,
        python=sys.version.split()[0],
        zlib=zlib.ZLIB_RUNTIME_VERSION,
        pyshp=shapefile.__version__,
        bytes=output.stat().st_size,
        sha256=digest(output),
    )
    output.with_suffix(".json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=DATA / "geographic_boundaries.db")
    parser.add_argument("--source-dir", type=Path, default=ROOT / "work/boundary-sources")
    args = parser.parse_args()
    print(json.dumps(generate(args.archive, args.output, args.source_dir), indent=2))
