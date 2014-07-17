# zerocycle.ingest
# Handles a variety of data ingestion and loading tasks
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Jul 14 23:20:57 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Handles a variety of data ingestion and loading tasks
"""

##########################################################################
## Imports
##########################################################################

from zerocycle.db.models import *
from zerocycle.exceptions import *
from zerocycle.db import create_session
from monthly import MonthlyReportReader
from accounts import AccountsReportReader
from base import ReportReader, CSVReportReader, ExcelReportReader

##########################################################################
## Module Constants
##########################################################################

READERS = {
    "MONTHLY":  MonthlyReportReader,
    "ACCOUNTS": AccountsReportReader,
    "EXCEL":    ExcelReportReader,
    "CSV":      CSVReportReader
}

##########################################################################
## Database access functions
##########################################################################

def insert_or_update(session, obj):
    """
    Temporary insert or update functionality; should go to the Manager.
    """

    if isinstance(obj, Route):
        # Do Route Lookup
        instance = session.query(Route).filter_by(name=obj.name).first()
    elif isinstance(obj, Pickup):
        # Do Pickup Lookup
        obj.route_id = obj.route.id
        instance = session.query(Pickup).filter_by(date=obj.date, route_id=obj.route.id, vehicle=obj.vehicle).first()
    else:
        instance = None

    if not instance:
        print "add"
        session.add(obj)
        return obj, True
    else:
        print "update"
        obj.id = instance.id
        session.merge(obj)
        return obj, False

##########################################################################
## Ingestion functions
##########################################################################

def ingest_report(report_type, path, **kwargs):
    """
    Accepts a report and a report_type, then creates a session and for
    every item that the report spits out, it saves the item to the database
    and then returns the item.

    If commit is passed into kwargs as False, this will not commit to the
    database, but instead just return the objects as they come.
    """

    commit      = kwargs.pop("commit", True)
    report_type = report_type.upper()
    if report_type not in READERS:
        raise IngestionException("No Report type called '%s'" % report_type)

    reader  = READERS[report_type](path, **kwargs)
    session = create_session()

    for item in reader:
        if isinstance(item, Base):
                yield insert_or_update(session, item)
        else:
            for obj in item:
                yield insert_or_update(session, obj)

    if commit:
        session.commit()
    session.close()

def ingest_monthly_report(path, **kwargs):
    """
    Alias for monthly reports ingestion.
    """
    for item in ingest_report('MONTHLY', path, **kwargs):
        yield item

def ingest_accounts_report(path, **kwargs):
    """
    Alias for accounts reports ingestion.
    """
    for item in ingest_report('ACCOUNTS', path, **kwargs):
        yield item
