# zerocycle.ingest.base
# Base API for ingestion related tasks.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Jul 14 23:21:29 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
Base API for ingestion related tasks.
"""

##########################################################################
## Imports
##########################################################################

from datetime import datetime
from xlrd import open_workbook
from zerocycle.db.models import *

##########################################################################
## Report Reader
##########################################################################

class ReportReader(object):
    """
    Reads a report and yields pickup objects
    """

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "<ReportReader at %s>" % self.path

    def __iter__(self):
        """
        Iterates through the items and returns Route, Pickup tuples
        """
        session = create_session()
        lookup  = {}
        for item in self.items():
            route = item.pop("route")
            supervisor = item.pop("supervisor")

            if route in lookup:
                route_id = lookup[route]
            else:
                route = Route(name=route, supervisor=supervisor)
                route = session.merge(route)
                lookup[route.name] = route

            pickup = Pickup(**item)
            pickup = session.merge(pickup)

            yield route, pickup

        session.commit()
        session.close()

    def items(self):
        """
        Denormalizes each row into Python dictionaries
        """
        supervisor  = None
        pickup_date = None

        for row in self.rows():
            front = row[0].strip().lower()
            if front == "daily date:":
                pickup_date = row[1].strip()
            elif front == "supervisor:":
                supervisor = row[1].strip()
            elif not front and row[1] and row[2] and row[3] and row[4]:
                yield {
                    "date": datetime.strptime(pickup_date, "%m/%d/%Y").date(),
                    "supervisor": supervisor,
                    "route": row[1].strip(),
                    "vehicle": row[2].strip(),
                    "miles": int(row[3].strip()),
                    "garbage": int(row[4])
                }

    def rows(self):
        """
        Handles Excel workbook access methods
        """
        workbook = open_workbook(self.path)
        for sheet in workbook.sheets():
            for row in xrange(sheet.nrows):
                yield [sheet.cell(row, col).value for col in xrange(sheet.ncols)]

if __name__ == '__main__':
    reader = ReportReader("/Users/benjamin/Repos/git/zerocycle/fixtures/march2014.xls")
    for item in reader: print item
