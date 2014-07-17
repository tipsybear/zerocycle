# zerocycle.db.managers
# Management methods for interacting with models
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jul 17 10:38:27 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Management methods for interacting with models
"""

##########################################################################
## Imports
##########################################################################

from zerocycle.db.models import *
from sqlalchemy.sql.expression import ClauseElement

##########################################################################
## Manager Class
##########################################################################

class Manager(object):
    """
    Provides Django-like queries on the models ...
    """

    def __init__(self, model):
        self.model = model

    def get_or_create(self, session, defaults=None, **kwargs):
        """
        Fetches the object from the database or creates it, returns the
        instance and a boolean indicating if it was created or not.
        """
        instance = session.query(self.model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            if defaults:
                params.update(defaults)
            instance = self.model(**params)
            return instance, True

class RoutesManager(Manager):

    def get_or_create(self, session, name):
        return super(RoutesManager, self).get_or_create(session, name=name)
