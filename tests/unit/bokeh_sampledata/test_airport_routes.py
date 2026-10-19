# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import pandas as pd

import bokeh_sampledata.airport_routes as m

ALL = (
    "airports",
    "routes",
)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_airports() -> None:
    assert isinstance(m.airports, pd.DataFrame)


def test_routes() -> None:
    assert isinstance(m.routes, pd.DataFrame)


def test_observed_route_endpoints_and_carriers() -> None:
    airports = m.airports.set_index("AirportID")
    assert airports.index.is_unique
    assert len(airports) >= 400
    assert airports.Latitude.between(-90, 90).all()
    assert airports.Longitude.between(-180, 180).all()
    routes = m.routes
    assert len(routes) >= 2000
    assert set(routes.SourceID) <= set(airports.index)
    assert set(routes.DestinationID) <= set(airports.index)
    assert (routes.SourceID != routes.DestinationID).all()
    assert routes.Airline.nunique() >= 10
    assert {"AA", "DL", "UA"} <= set(routes.Airline)
    assert "DEMO" not in set(routes.Airline)
    assert ((routes.Source == "ATL") & (routes.Destination == "LAX")).any()
    assert (routes.Source.to_numpy() == airports.loc[routes.SourceID, "IATA"].to_numpy()).all()
    assert (routes.Destination.to_numpy() == airports.loc[routes.DestinationID, "IATA"].to_numpy()).all()


def test_legacy_text_columns() -> None:
    for column in ("Timezone", "DST", "TZ"):
        assert pd.api.types.is_string_dtype(m.airports[column].dtype)
    for column in ("AirlineID", "Codeshare", "Equipment"):
        assert pd.api.types.is_string_dtype(m.routes[column].dtype)
