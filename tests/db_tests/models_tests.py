# tests.db_tests.models_tests
# Test the models described using declarative base.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Jul 14 22:44:53 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models_tests.py [] benjamin@bengfort.com $

"""
Test the models described using declarative base.
"""

##########################################################################
## Imports
##########################################################################

import unittest

from zerocycle.db.models import *

##########################################################################
## TestCases
##########################################################################

class ConnectionTests(unittest.TestCase):
    """
    Tests for the connection helper functions
    """

    def test_engine_url(self):
        """
        Check that the engine has constructed the right URL
        """
        engine = get_engine()
        self.assertEqual(str(engine.url), "postgresql://postgres:@127.0.0.1:5432/zerocycle")
