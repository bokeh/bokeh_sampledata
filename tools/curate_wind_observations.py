# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Curate a downloaded NOAA METAR cache without fetching or inventing observations."""

from __future__ import annotations

import argparse
import csv
import gzip
import io
from pathlib import Path

COLUMNS = {
    "station_id": "station",
    "observation_time": "time",
    "latitude": "latitude",
    "longitude": "longitude",
    "wind_dir_degrees": "direction",
    "wind_speed_kt": "speed",
    "wind_gust_kt": "gust",
    "temp_c": "temperature",
    "dewpoint_c": "dewpoint",
    "elevation_m": "elevation",
}


def curate(source: Path, target: Path) -> None:
    with gzip.open(source, "rt", encoding="utf-8", newline="") as stream:
        rows = sorted(csv.DictReader(stream), key=lambda row: row["station_id"])
    for row in rows:
        if row["latitude"] and not -90 <= float(row["latitude"]) <= 90:
            row["latitude"] = row["longitude"] = ""
        if row["elevation_m"] == "9999":
            row["elevation_m"] = ""
    with target.open("wb") as output:
        with gzip.GzipFile(filename="", fileobj=output, mode="wb", mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                writer = csv.writer(text, lineterminator="\n")
                writer.writerow(COLUMNS.values())
                writer.writerows([row[column] for column in COLUMNS] for row in rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Downloaded metars.cache.csv.gz")
    parser.add_argument("target", type=Path, help="Curated wind_observations.csv.gz")
    args = parser.parse_args()
    curate(args.source, args.target)
