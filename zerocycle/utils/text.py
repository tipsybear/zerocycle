# zerocycle.utils.text
# A text helper methods lib for intense text work
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jul 16 16:14:55 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: text.py [] benjamin@bengfort.com $

"""
A text helper methods lib for intense text work
"""

##########################################################################
## Imports
##########################################################################

import re
import sys
import string
import unicodedata

##########################################################################
## Helper functions
##########################################################################

def depunctuate(s):
    """
    Remove all punctuation from a string.
    """
    if s is None:
        return None

    elif isinstance(s, str):
        return s.translate(string.maketrans("",""), string.punctuation)

    elif isinstance(s, unicode):
        tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                if unicodedata.category(unichr(i)).startswith('P'))
        return s.translate(tbl)

    else:
        raise TypeError("Unknown type to depunctuate, '%s'" % type(s))

def grayspace(s):
    """
    Replace all whitespace (tabs, newlines, multiple spaces) with a single
    space character, then strip off any trailing space at the end.
    """
    if s is None: return None
    return re.sub( '\s+', ' ', s ).strip()

def normalize(text):
    """
    This attempts to normalize a piece of text for purposes of comparison
    by doing the following things to the text:

        * Removing all punctuation
        * Replacing all whitespace with a single space
        * Making all characters lowercase.

    This will allow for case-insensitive, punctuation-insensitive,
    whitespace-insensitive string comparisons.
    """
    if text is None: return None
    text = depunctuate(text)
    text = grayspace(text)
    return text.lower()

def compare(apples, oranges):
    """
    Compares two pieces of text by normalizing them, and then comparing.
    """
    return normalize(apples) == normalize(oranges)

