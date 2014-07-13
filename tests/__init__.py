# tests
# Test package for the Zerocycle project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 13 08:40:56 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Test package for the Zerocycle project
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Test Cases
##########################################################################

class InitializationTests(unittest.TestCase):

    def test_initialization(self):
        """
        Assert the world is sane by verifying a fact, 2+3=5
        """
        self.assertEqual(2+3, 5)

    def test_import(self):
        """
        Test our ability to import the zerocycle package
        """
        try:
            import zerocycle
        except ImportError:
            self.fail("Could not import zerocycle package")
