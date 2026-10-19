# -----------------------------------------------------------------------------
# Copyright (c) Bokeh Contributors
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""US federal and selected cultural holidays, parsed with ``icalendar``.

License: BSD-3-Clause. Dates are independently calculated from calendar rules.
Federal holidays follow the `OPM calendar
<https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/>`_.
The legacy ``(US-OPM)`` marker denotes observed dates for Monday-Friday federal
employees, moving Saturday holidays to Friday and Sunday holidays to Monday.

Nominal holiday years run from 2000 through 2030. New Year's Day 2000 is observed
on December 31, 1999. Selected cultural and Easter-based Christian observances
use their calendar dates. This is an illustrative calendar, not an exhaustive
employment or religious calendar.

This module contains one list, ``us_holidays``, of ``(datetime.date, name)`` pairs.

.. bokeh-sampledata-xref:: us_holidays

"""

from __future__ import annotations

import icalendar as ic

from . import package_path

__all__ = ("us_holidays",)

with open(package_path("USHolidays.ics"), encoding="utf-8") as f:
    data = ic.Calendar.from_ical(f.read())

us_holidays = sorted((elt.get("dtstart").dt, str(elt.get("summary"))) for elt in data.walk() if elt.name == "VEVENT")
