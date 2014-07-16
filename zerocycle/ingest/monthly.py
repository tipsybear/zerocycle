# zerocycle.ingest.monthly
# Report reader for monthly supervisor reports
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jul 16 15:10:50 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: monthly.py [] benjamin@bengfort.com $

"""
Report reader for monthly supervisor reports
"""

##########################################################################
## Imports
##########################################################################

import warnings

from datetime import datetime
from zerocycle.utils import text
from zerocycle.db.models import *
from zerocycle.exceptions import *
from zerocycle.ingest.base import ExcelReportReader

##########################################################################
## MonthlyReportReader
##########################################################################

class MonthlyReportReader(ExcelReportReader):

    def __init__(self, *args, **kwargs):
        """
        Can customize the date format of a report.
        """
        self.datefmt  = kwargs.pop("date_format", "%m/%d/%Y")
        super(MonthlyReportReader, self).__init__(*args, **kwargs)

    def __iter__(self):
        """
        Iterates through the items and returns Route, Pickup tuples. If
        warnings is False, then this code will halt on exceptions. If
        warnings is True then the method will print warnings about rows
        unless the verbose is set to false, in which case the warnings
        will be returned to the user.
        """
        lookup  = {}
        for item in self.items():
            route = item.pop("route")
            supervisor = item.pop("supervisor")

            if route in lookup:
                route = lookup[route]
            else:
                route = Route(name=route, supervisor=supervisor)
                lookup[route.name] = route

            pickup = Pickup(**item)
            pickup.route = route

            yield route, pickup

    def items(self, **kwargs):
        """
        Denormalizes each row into Python dictionaries
        """

        self._current_pickup_date = None
        self._current_supervisor  = None

        for row in self.rows(**kwargs):
            item = self.handle_item(row)
            if item is not None:
                yield item

    def handle_row(self, row):
        """
        Inspects any interesting rows and sets data handling properties on
        the class if needed. For example, this function will identify the
        pickup_date row as well as the supervisor row and store them for
        iteration over the class.
        """
        row = super(MonthlyReportReader, self).handle_row(row)

        if row[0] is None and None not in row[1:]:
            # Discovered a record row (hopefully) where the first cell is
            # blank and none of the other cells are blank.
            return row

        if [None] * len(row) == row:
            # Discovered a completely empty row (full of None)
            return None

        if text.compare("daily date", row[0]):
            # Discovered a daily date row, set the pickup date and move on
            self._current_pickup_date = datetime.strptime(row[1], self.datefmt).date()
            return None

        if text.compare("supervisor", row[0]):
            # Discovered a supervisor row, set the supervisor and move on
            self._current_supervisor  = row[1]
            return None

        if text.compare("daily total", row[0]):
            # Discovered a daily total row, we could do a checksum
            return None

        if text.compare("supervisor total", row[0]):
            # Discovered a supervisor total row, we could do a checksum
            return None

        if text.compare("supervisor daily report", row[0]):
            # Discovered the header row, move on
            return None

        # Ok, if we've gotten to this point, we don't know what the row is.
        message = "unknown monthly report row: \"%s\"" % "\t".join(str(item) for item in row)
        warnings.warn(message ,UnparsableRow)
        return None

    def handle_item(self, item):
        """
        Denormalizes the item into a Python dictionary.
        """
        return {
            "date": self._current_pickup_date,
            "supervisor": self._current_supervisor,
            "route": item[1],
            "vehicle": item[2],
            "miles": int(item[3]),
            "garbage": int(item[4])
        }


if __name__ == '__main__':
    import os

    FIXTURE = os.path.join(os.path.dirname(__file__), "../../fixtures/march2014.xls")
    reader = MonthlyReportReader(FIXTURE)
    for item in reader:
        print "%s: %s" % item
