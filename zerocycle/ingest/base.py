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

import os
import unicodecsv as csv

from xlrd import open_workbook
from zerocycle.exceptions import *

##########################################################################
## Report Reader
##########################################################################

class ReportReader(object):
    """
    Base report reader class - it implements methods for accessing and
    iterating through reports that come from various cities. Provides a
    standard interface for all ReportReader objects.
    """

    def __init__(self, path, **kwargs):
        self.path = path
        self.encoding = kwargs.pop('encoding', None)

    def __str__(self):
        return "<%s at %s>" % (self.__class__.__name__, self.path)

    def __iter__(self):
        """
        Iterate through all items in the report.
        """
        for item in self.items():
            yield item

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        value = os.path.expanduser(value)
        value = os.path.expandvars(value)
        value = os.path.abspath(os.path.normpath(value))

        if not os.path.exists(value) or not os.path.isfile(value):
            raise ReportNotFound("Could not find a report at '%s'" % value)

        self._path = value

    def rows(self):
        """
        Access each row of the report, line-by-line. This method is an
        internal access method because report items can be multi-line and
        may require additional processing. Note that rows are always
        passed to the `handle_row` method, which can be implemented by
        subclasses to do per-row processing.
        """
        raise NotImplementedError("Subclasses must implement a rows method "
                                  "that makes a per-row call to self.handle_row")

    def handle_row(self, row):
        """
        Subclasses may choose to handle each row individually rather than
        in aggregate by implementing this per row method. This method must
        return a row. Returning `None` is the equivalent of `continue`.
        """
        return row

    def items(self):
        """
        Access each item of the report. This method is an external access
        method, and in fact is called by `__iter__` for easy access. This
        method should use the `rows` method to construct an object, even
        if the construction is multiline.
        """
        raise NotImplementedError("Subclasses must implement an items method "
                                  "that makes a per-row call to self.handle_item")

    def handle_item(self, item):
        """
        Subclasses may choose to handle each item individually rather than
        in aggregate by implementing this per item method. This method
        must return an item. Returning `None` is the equivalent of
        `continue`.
        """
        return item

##########################################################################
## CSVReportReader
##########################################################################

class CSVReportReader(ReportReader):
    """
    A report reader that wraps a CSV report and implements `rows` and
    `items` in order to allow subclasses to not have to deal with a csv.
    """

    def __init__(self, path, delimiter=",", quotechar="\"", **kwargs):
        self.delimiter  = delimiter
        self.quotechar  = quotechar
        self.header     = kwargs.pop('header', False)

        kwargs['encoding'] = kwargs.get('encoding', 'utf-8')
        super(CSVReportReader, self).__init__(path, **kwargs)

    def rows(self, **kwargs):
        """
        Uses the unicodecsv reader to read any encoding of CSV file.
        Yields dictionaries or tuples based on the existence of a header.
        """
        kwargs['encoding']  = kwargs.get('encoding', self.encoding)
        kwargs['delimiter'] = kwargs.get('delimiter', self.delimiter)
        kwargs['quotechar'] = kwargs.get('quotechar', self.quotechar)

        with open(self.path, 'rU') as data:
            reader = csv.DictReader(data, **kwargs) if self.header else csv.reader(data, **kwargs)
            for row in reader:
                row = self.handle_row(row)
                if row is not None:
                    yield row

    def items(self, **kwargs):
        """
        Pass-through for CSV rows since CSV rows are typically entities.
        """
        for item in self.rows(**kwargs):
            item = self.handle_item(item)
            if item is not None:
                yield item

##########################################################################
## ExcelReportReader
##########################################################################

class ExcelReportReader(ReportReader):
    """
    A report reader that wraps an Excel report and implements `rows` and
    `items` in order to allow subclasses to not have to deal with the
    Excel file. This class treats an Excel file like a fancy CSV.
    """

    def rows(self, **kwargs):
        """
        Handles Excel workbook access methods. Currently this method
        iterates through every single sheet in a workbook, returning all
        of the rows from the Excel file.
        """
        workbook = open_workbook(self.path)
        for sheet in workbook.sheets():
            for ridx in xrange(sheet.nrows):
                row = [sheet.cell(ridx, cidx) for cidx in xrange(sheet.ncols)]
                row = self.handle_row(row)
                if row is not None:
                    yield row

    def handle_row(self, row):
        """
        Strips off spaces in every row for uniformity. Replaces empty rows
        with "None" - this is a text handling method, but leaves all
        number values alone.
        """

        def handle_cell(cell):
            """
            Handles individual cells.
            """
            # These are blank/empty cells
            if cell.ctype in (0, 5, 6):
                return None

            # This is the boolean type, cast to a bool.
            if cell.ctype == 4:
                return bool(cell.value)

            # Text processing type
            if cell.ctype == 1:
                return cell.value.strip()

            # Fall through, the rest are numbers
            return cell.value

        return [handle_cell(cell) for cell in row]

    def items(self, **kwargs):
        """
        Pass-through for Excel rows since Excel rows are typically entities.
        """
        for item in self.rows(**kwargs):
            item = self.handle_item(item)
            if item is not None:
                yield item

##########################################################################
## Main and Testing
##########################################################################

if __name__ == '__main__':
    pass
