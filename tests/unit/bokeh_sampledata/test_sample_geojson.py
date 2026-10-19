# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import json
from math import isfinite

import bokeh_sampledata.sample_geojson as m

ALL = ("geojson",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_geojson() -> None:
    assert isinstance(m.geojson, str)


def test_historical_area_team_features() -> None:
    collection = json.loads(m.geojson)
    assert collection["type"] == "FeatureCollection"
    features = collection["features"]
    assert len(features) == 25
    codes = set()
    for feature in features:
        assert feature["type"] == "Feature"
        properties = feature["properties"]
        assert properties["OrganisationType"] == "Area Team"
        assert {"OrganisationCode", "OrganisationType", "OrganisationName"} <= properties.keys()
        assert properties["OrganisationName"]
        codes.add(properties["OrganisationCode"])
        geometry = feature["geometry"]
        assert geometry["type"] == "Point"
        longitude, latitude = geometry["coordinates"]
        assert isfinite(longitude) and -180 <= longitude <= 180
        assert isfinite(latitude) and -90 <= latitude <= 90
    assert len(codes) == len(features)
    assert "Q64" in codes
