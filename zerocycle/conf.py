# zerocycle.conf
# A simple configuration module for Zerocycle
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 19 10:30:03 2013 -0500
#
# Copyright (C) 2014 Tipsy Bear
# For license information, see LICENSE.txt
#
# ID: conf.py [] benjamin@bengfort.com $

"""
Configuration class for specifying zerocycle specific optional items via a
YAML configuration file format. The main configuration class provides
utilities for loading the configuration from disk and iterating across all
the settings. Subclasses of the Configuration specify defaults that can be
updated via the configuration files.

General usage:

    from zerocycle.conf import settings
    mysetting = settings.get('mysetting', default)

You can also get settings via a dictionary like access:

    mysetting = settings['mysetting']

However, this will raise an exception if the setting is not found.

Note: Keys are CASE insensitive

Note: Settings can be modified directly by settings.mysetting = newsetting
however, this is not recommended, and settings should be fetched via the
dictionary-like access.
"""

##########################################################################
## Imports
##########################################################################

import os
import yaml

from copy import deepcopy

##########################################################################
## Configuration Base Class
##########################################################################

class Configuration(object):
    """
    Base configuration class specifies how configurations should be
    handled and provides helper methods for iterating through options and
    configuring the base class.

    Subclasses should provide defaults for the various configurations as
    directly set class level properties. Note, however, that ANY directive
    set in a configuration file (whether or not it has a default) will be
    added to the configuration.

    Example:

        class MyConfig(Configuration):

            mysetting = True
            logpath   = "/var/log/myapp.log"
            appname   = "MyApp"

    The configuration is then loaded via the classmethod `load`:

        settings = MyConfig.load()

    Access to properties is done two ways:

        settings['mysetting']
        settings.get('mysetting', True)

    Note: None settings are not allowed!
    """

    CONF_PATHS = [
        '/etc/zerocycle/app.yaml',                        # The global configuration
        os.path.expandvars('$HOME/.zerocycle/app.yaml'),  # User specific configuration
        os.path.abspath('conf/zerocycle.yaml'),           # Local directory configuration
        os.path.abspath('.zerocycle.yaml')                # Local directory configuration
    ]

    @classmethod
    def load(klass):
        """
        Insantiates the configuration by attempting to load the
        configuration from YAML files specified by the CONF_PATH module
        variable. This should be the main entry point for configuration.
        """
        config = klass()
        for path in klass.CONF_PATHS:
            if os.path.exists(path):
                with open(path, 'r') as conf:
                    config.configure(yaml.load(conf))
        return config

    def configure(self, conf={}):
        """
        Allows updating of the configuration via a dictionary of
        configuration terms or a configuration object. Generally speaking,
        this method is utilized to configure the object from a JSON or
        YAML parsing.
        """
        if not conf: return
        if isinstance(conf, Configuration):
            conf = dict(conf.options())

        keys = conf.keys()
        for key in keys:
            opt = self.get(key, None)
            if isinstance(opt, Configuration):
                opt.configure(conf.pop(key))
        self.__dict__.update(conf)

    def options(self):
        """
        Returns an iterable of sorted option names in order to loop
        through all the configuration directives specified in the class.
        """
        keys = self.__class__.__dict__.copy()
        keys.update(self.__dict__)
        keys = keys.keys()
        keys.sort()

        for opt in keys:
            val = self.get(opt)
            if val is not None: yield opt, val

    def get(self, key, default=None):
        """
        Fetches a key from the configuration without raising a KeyError
        exception if the key doesn't exist in the config, instead it
        returns the default (None).
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        """
        Main configuration access method. Performs a case insensitive
        lookup of the key on the class, filtering methods and pseudo
        private properties. Raises KeyError if not found. Note, this makes
        all properties that are uppercase invisible to the options.
        """
        key = key.lower()
        if hasattr(self, key):
            attr = getattr(self, key)
            if not callable(attr) and not key.startswith('_'):
                return attr
        raise KeyError("%s has no configuration '%s'" % (self.__class__.__name__, key))

    def __repr__(self):
        return str(self)

    def __str__(self):
        s = ""
        for opt, val in self.options():
            r = repr(val)
            r = " ".join(r.split())
            wlen = 76-max(len(opt),10)
            if len(r) > wlen:
                r = r[:wlen-3]+"..."
            s += "%-10s = %s\n" % (opt, r)
        return s[:-1]

##########################################################################
## LoggingConfiguration
##########################################################################

##########################################################################
## DatabaseConfiguration
##########################################################################

class DatabaseConfiguration(Configuration):
    """
    This object contains the default configuration to our database.

    NOTE: The default user and password is the test user/password.

    name: the name of the database
    user: the user to connect to the database
    password: the password for user connection
    host: the hostname of the database
    port: the port of the database
    """
    scheme          = "postgresql"
    name            = "zerocycle"
    user            = "postgres"
    password        = ""
    host            = "127.0.0.1"
    port            = 5432

    @property
    def uri(self):
        if self.scheme == 'sqlite':
            if self.name:
                return "{scheme}:///{db}".format(scheme=self.scheme, db=self.name)
            return "{scheme}://"

        urifmt = "{scheme}://{user}:{passwd}@{host}:{port}/{db}"
        return urifmt.format(
            scheme = self.scheme,
            user   = self.user,
            passwd = self.password,
            host   = self.host,
            port   = self.port,
            db     = self.name
        )

##########################################################################
## Zerocycle Configuration Defaults
##########################################################################

class ZerocycleConfiguration(Configuration):
    """
    This object contains the default configuration of Zerocycle.

    debug: allow debug checking
    testing: are we in testing mode?
    """
    debug           = True
    testing         = False
    database        = DatabaseConfiguration()

class TestingConfiguration(ZerocycleConfiguration):
    """
    This object contains the default configuration for Testing.
    """

    debug           = True
    testing         = True
    database        = DatabaseConfiguration()

##########################################################################
## Import this loaded Configuration
##########################################################################

settings = ZerocycleConfiguration.load()
if bool(int(os.environ.get("ZEROCYCLE_TESTING", 0))):
    settings.configure(TestingConfiguration())

if __name__ == '__main__':
    print settings
