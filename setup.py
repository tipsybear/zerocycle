#!/usr/bin/env python
# setup
# Setuptools installation script for Zerocycle project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 13 08:43:16 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: setup.py [] benjamin@bengfort.com $

"""
Setuptools installation script for Zerocycle project
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\". "
                      "Please install the setuptools package.")

##########################################################################
## Configuration Details
##########################################################################

## Set up project variables
project  = "zerocycle"
packages = [p for p in find_packages(".") if p.startswith(project)]
requires = None

## Load requirements
with open('requirements.txt', 'r') as reqfile:
    requires = [line.strip() for line in reqfile]

## Classify the project
classifiers = (
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Environment :: Console',
    'Framework :: Flask',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
)

## Configure the PyPy index
config = {
    "name": "Zerocycle",
    "version": "0.1",
    "description": "Zerocycle analysis toolkit",
    "author": "Benjamin Bengfort",
    "author_email": "benjamin@bengfort.com",
    "url": "https://github.com/tipsybear/zerocycle",
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "scripts": ["bin/zerocycle"],
    "zip_safe": False,
}

##########################################################################
## Execute the installation script
##########################################################################

setup(**config)
