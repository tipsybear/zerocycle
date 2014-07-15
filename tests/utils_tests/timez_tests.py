# tests.utils_tests.timez_tests
# Tests for the timez utility package
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Nov 11 12:48:23 2013 -0500
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: timez_tests.py [] benjamin@bengfort.com $

"""
Tests for the timez utility package
"""

##########################################################################
## Imports
##########################################################################

import unittest

from zerocycle.utils.timez import *
from dateutil.tz import tzlocal, tzutc
from datetime import datetime, timedelta

class TimezTest(unittest.TestCase):

    def setUp(self):
        self.localnow = datetime.now(tzlocal()).replace(microsecond=0)
        self.utcnow   = self.localnow.astimezone(tzutc())

    def tearDown(self):
        self.localnow = self.utcnow = None

    def test_strptimez(self):
        """
        Assert that strptimez returns a tz aware utc datetime
        """
        dtfmt = "%a %b %d %H:%M:%S %Y %z"
        dtstr = self.localnow.strftime(dtfmt)
        self.assertEqual(strptimez(dtstr, dtfmt), self.utcnow)

    def test_strptimez_no_z(self):
        """
        Assert that strptimez works with no '%z'

        This should return a timezone naive datetime
        """
        dtfmt = "%a %b %d %H:%M:%S %Y"
        dtstr = self.localnow.strftime(dtfmt)
        self.assertEqual(strptimez(dtstr, dtfmt), self.localnow.replace(tzinfo=None))

    def test_strptimez_no_space(self):
        """
        Non-space delimited '%z' works
        """
        dtfmt = "%Y-%m-%dT%H:%M:%S%z"
        dtstr = self.localnow.strftime(dtfmt)
        self.assertEqual(strptimez(dtstr, dtfmt), self.utcnow)

    def test_begin_z(self):
        """
        Test fmt that begins with '%z'
        """
        dtfmt = "%z %H:%M:%S for %Y-%m-%d"
        dtstr = self.localnow.strftime(dtfmt)
        self.assertEqual(strptimez(dtstr, dtfmt), self.utcnow)

    def test_middle_z(self):
        """
        Test fmt that contains '%z'
        """
        dtfmt = "time is: %H:%M:%S %z on %Y-%m-%d "
        dtstr = self.localnow.strftime(dtfmt)
        self.assertEqual(strptimez(dtstr, dtfmt), self.utcnow)

class ClockTest(unittest.TestCase):

    def get_now_times(self):
        localnow = datetime.now(tzlocal()).replace(microsecond=0)
        utcnow   = localnow.astimezone(tzutc())
        return (localnow, utcnow)

    def test_clock_localnow(self):
        """
        Local time computation matches
        """
        testrnow = self.get_now_times()[0].replace(second=0)
        clocknow = Clock.localnow().replace(second=0,microsecond=0)
        self.assertEqual(testrnow, clocknow)

    def test_clock_utcnow(self):
        """
        UTC time computation matches
        """
        testrnow = self.get_now_times()[1].replace(second=0)
        clocknow = Clock.utcnow().replace(second=0,microsecond=0)
        self.assertEqual(testrnow, clocknow)

    def test_local_offset(self):
        """
        Assert local time is offset UTC
        """
        localnow = Clock.localnow().replace(second=0, microsecond=0)
        utcnow = Clock.utcnow().replace(second=0, microsecond=0)

        offset = int(localnow.strftime('%z'))
        delta  = timedelta(hours = offset/100)
        offnow = localnow - delta

        self.assertEqual(offnow.replace(tzinfo=None), utcnow.replace(tzinfo=None))

    def test_local_utc_diff(self):
        """
        Assert local time is not UTC time
        """
        localnow = Clock.localnow().replace(second=0, microsecond=0)
        utcnow = Clock.utcnow().replace(second=0, microsecond=0)

        if localnow.strftime('%z') == utcnow.strftime('%z'):
            self.assertEqual(localnow, utcnow)
        else:
            self.assertNotEqual(localnow.replace(tzinfo=None), utcnow.replace(tzinfo=None))

    def test_clock_format(self):
        """
        Format works with fmt string
        """
        fmt = "%Y-%m-%dT%H:%M:%S%z"
        dts = self.get_now_times()[0]
        clk = Clock()
        self.assertEqual(dts.strftime(fmt), clk.format(dts, fmt))

    def test_clock_simple_format(self):
        """
        Test named formats
        """
        fmt = "%Y-%m-%dT%H:%M:%S%z"
        dts = self.get_now_times()[0]
        clk = Clock()
        self.assertEqual(dts.strftime(fmt), clk.format(dts, "iso"))

    def test_default_format(self):
        """
        Assert defaults can be passed in
        """
        fmt = "%Y-%m-%dT%H:%M:%S%z"
        dts = self.get_now_times()[0]
        clk = Clock(default="iso")
        self.assertEqual(dts.strftime(fmt), clk.format(dts))

    def test_isoutc_formatter(self):
        """
        Test ISO UTC formatter
        """
        clk = Clock("iso", local=False)
        lcl = self.get_now_times()[1]
        self.assertEqual(str(clk), lcl.strftime("%Y-%m-%dT%H:%M:%S%z"))
