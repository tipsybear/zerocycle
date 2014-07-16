# tests.utils_tests.text_tests
# Tests for the text helpers library
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jul 16 16:31:25 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: text_tests.py [] benjamin@bengfort.com $

"""
Tests for the text helpers library
"""

##########################################################################
## Imports
##########################################################################

import string
import unittest

from zerocycle.utils import text

##########################################################################
## TestCase
##########################################################################

class TextUtilsTests(unittest.TestCase):

    def test_depunctuate(self):
        """
        Test the depunctuate function.
        """

        original = "A string, named Mr. String, who has punctuation?!"
        expected = "A string named Mr String who has punctuation"

        self.assertEqual(expected, text.depunctuate(original))

    def test_depunctuate_chars(self):
        """
        Test expected punctuation removal
        """

        original = "?!,.+-_@$<>/[]\"':;{}|\\%#^&*()~`"
        expected = ""

        self.assertEqual(expected, text.depunctuate(original))

    def test_depunctuate_unicode(self):
        """
        Test punctuation removal on unicode
        """

        original = u"A string, named Mr. String, who has punctuation?!"
        expected = u"A string named Mr String who has punctuation"

        self.assertEqual(expected, text.depunctuate(original))

    def test_depunctuate_exception(self):
        """
        Test depunctuate on type checking
        """

        with self.assertRaises(TypeError):
            text.depunctuate(1)

    def test_depunctuate_none(self):
        """
        Test depunctuate on None
        """
        self.assertIsNone(text.depunctuate(None))

    def test_grayspace(self):
        """
        Test the grayspace method
        """
        original = "bob    went  to the\tstore\n    with   a friend     "
        expected = "bob went to the store with a friend"

        self.assertEqual(expected, text.grayspace(original))

    def test_grayspace_unicode(self):
        """
        Test the grayspace method on unicode
        """
        original = u"bob    went  to the\tstore\n    with   a friend     "
        expected = u"bob went to the store with a friend"

        self.assertEqual(expected, text.grayspace(original))

    def test_grayspace_none(self):
        """
        Test grayspace on None
        """
        self.assertIsNone(text.grayspace(None))

    def test_normalize(self):
        """
        Test the normalize method
        """
        original = "BOB    went,  to the?-\tstore\n    wIth   a friend!!     "
        expected = "bob went to the store with a friend"

        self.assertEqual(expected, text.normalize(original))

    def test_normalize_unicode(self):
        """
        Test the normalize method on unicode
        """
        original = u"BOB    went,  to the?-\tstore\n    wIth   a friend!!     "
        expected = u"bob went to the store with a friend"

        self.assertEqual(expected, text.normalize(original))

    def test_normalize_none(self):
        """
        Test normalize on None
        """
        self.assertIsNone(text.normalize(None))

    def test_compare(self):
        """
        Test the string comparison function
        """
        original = "BOB    went,  to the?-\tstore\n    wIth   a friend!!     "
        expected = "bob went to the store with a friend"

        self.assertTrue(text.compare(original, expected))
