# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

import bokeh_sampledata.haar_cascade as m

ALL = ("frontalface_default_path",)


def test___all__() -> None:
    assert m.__all__ == ALL


def test_data() -> None:
    assert isinstance(m.frontalface_default_path, Path)


def test_frontal_face_cascade_structure() -> None:
    assert m.frontalface_default_path.is_file()
    root = ElementTree.parse(m.frontalface_default_path).getroot()
    assert root.tag == "opencv_storage"
    cascade = root.find("cascade")
    assert cascade is not None
    assert cascade.attrib["type_id"] == "opencv-cascade-classifier"
    assert cascade.findtext("width") == cascade.findtext("height") == "24"
    assert cascade.findtext("featureType") == "HAAR"
    stages = cascade.find("stages")
    features = cascade.find("features")
    assert stages is not None and len(stages) == 25
    assert features is not None and len(features) > 0


def test_intel_notice_retained() -> None:
    text = m.frontalface_default_path.read_text(encoding="utf-8")
    assert "Intel License Agreement" in text
    assert "Copyright (C) 2000, Intel Corporation, all rights reserved." in text
