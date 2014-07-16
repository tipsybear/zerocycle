# zerocycle.exceptions
# Exceptions hierarchy for the zerocycle library
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jul 16 15:29:19 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Exceptions hierarchy for the zerocycle library
"""

##########################################################################
## Base exception
##########################################################################

class ZerocycleException(Exception):
    """
    Base exception in the zerocycle exception hierarchy.
    """
    pass

class ZerocycleWarning(Warning):
    """
    Base warning class in the zerocycle warning hierarchy.
    """
    pass

##########################################################################
## Ingestion exceptions
##########################################################################

class IngestionException(ZerocycleException):
    """
    A problem occurred with ingesting a particular report.
    """
    pass

class IngestionWarning(ZerocycleWarning):
    """
    There is a nonfatal problem with some piece of ingestion.
    """
    pass

class ReportNotFound(IngestionException):
    """
    No report was found on the filesystem in the specified location.
    """
    pass

class UnparsableRow(IngestionWarning):
    """
    Could not parse a row from the file
    """
    pass
