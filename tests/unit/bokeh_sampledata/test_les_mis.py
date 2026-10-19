# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

import bokeh_sampledata.les_mis as m

ALL = ("data",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_data() -> None:
    assert isinstance(m.data, dict)

    assert set(m.data.keys()) == {"links", "nodes"}


def test_character_graph_references() -> None:
    nodes = m.data["nodes"]
    links = m.data["links"]
    assert len(nodes) == 77
    assert len(links) == 254
    assert len({node["name"] for node in nodes}) == len(nodes)
    assert nodes[0]["name"] == "Myriel"
    for link in links:
        assert isinstance(link["source"], int) and 0 <= link["source"] < len(nodes)
        assert isinstance(link["target"], int) and 0 <= link["target"] < len(nodes)
        assert link["value"] > 0


def test_graph_is_connected() -> None:
    reached = {0}
    while True:
        adjacent = set(reached)
        for edge in m.data["links"]:
            if edge["source"] in reached or edge["target"] in reached:
                adjacent.update((edge["source"], edge["target"]))
        if reached == adjacent:
            break
        reached = adjacent
    assert reached == set(range(len(m.data["nodes"])))


def test_bishop_valjean_encounter() -> None:
    names = [node["name"] for node in m.data["nodes"]]
    pair = {names.index("Myriel"), names.index("Valjean")}
    assert any({link["source"], link["target"]} == pair and link["value"] == 5 for link in m.data["links"])
