# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""Provide a pretrained Haar cascade for frontal face detection.

License: Intel License Agreement for Open Source Computer Vision Library
(a BSD-style license), embedded in the XML file and reproduced in
``licenses/LicenseRef-Intel-OpenCV.txt``. Copyright (C) 2000, Intel
Corporation. The classifier was created by Rainer Lienhart and is distributed
unmodified from `OpenCV 4.4.0
<https://github.com/opencv/opencv/blob/4.4.0/data/haarcascades/haarcascade_frontalface_default.xml>`_.
Source hashes and provenance are recorded in ``licenses/datasets.json``.

This module contains one attribute, ``frontalface_default_path``, a path usable
with OpenCV's ``CascadeClassifier`` and ``detectMultiScale``.

.. bokeh-sampledata-xref:: haar_cascade

"""

from __future__ import annotations

from . import package_path

__all__ = ("frontalface_default_path",)

frontalface_default_path = package_path("haarcascade_frontalface_default.xml")
