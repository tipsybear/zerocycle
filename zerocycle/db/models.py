# zerocycle.db.models
# Models to interact with the database by.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Zerocycle Models for interacting with the database. These models use the
SQLAlchemy delcarative base extension to define them in a "Django-like"
way.

@todo: Should we have a Report model to track reports?
"""

##########################################################################
## Imports
##########################################################################

from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, Unicode, UnicodeText
from sqlalchemy import DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from zerocycle.conf import settings
from zerocycle.utils.timez import Clock
from datetime import datetime


##########################################################################
## Module Constants
##########################################################################

Base = declarative_base() # SQLAlchemy declarative extension

##########################################################################
## Models
##########################################################################

class Route(Base):
    """
    Stores information about Austin city garbage truck routes.
    """

    __tablename__ = 'routes'

    id            = Column(Integer, primary_key=True, nullable=False)
    name          = Column(Unicode(50), unique=True, nullable=False)
    supervisor    = Column(Unicode(50), nullable=True)
    locations     = Column(Integer, nullable=True)
    created       = Column(DateTime(timezone=True), default=Clock.localnow)
    updated       = Column(DateTime(timezone=True), default=Clock.localnow, onupdate=Clock.localnow)

    def __str__(self):
        return "Route %s" % self.name

class Pickup(Base):
    """
    Stores information about daily trash pickups in Austin.
    """

    __tablename__  = 'pickups'
    __table_args__ = (
        UniqueConstraint('route_id', 'date', 'vehicle'),
    )

    id            = Column(Integer, primary_key=True, nullable=False)
    date          = Column(Date, nullable=False)
    route_id      = Column(Integer, ForeignKey('routes.id'), nullable=False)
    route         = relationship('Route', backref='pickups')
    vehicle       = Column(Unicode(20))
    miles         = Column(Integer)
    garbage       = Column(Integer)
    created       = Column(DateTime(timezone=True), default=Clock.localnow)
    updated       = Column(DateTime(timezone=True), default=Clock.localnow, onupdate=Clock.localnow)

    def __str__(self):
        return "Pickup on %s for route %s" % (Clock().format(self.date, "isodate"), self.route)

##########################################################################
## Database helper methods
##########################################################################

def get_engine(uri=None):
    uri = uri or settings.get('database').uri
    return create_engine(uri)

def syncdb(uri=None):
    engine = get_engine(uri)
    Base.metadata.create_all(engine)
    return engine.url

## Descriptor for creating and maintaining sessions
class SessionFactory(object):

    def __init__(self):
        self.engine  = None
        self.factory = None

    def __call__(self):
        if self.engine is None:
            self.engine  = get_engine()
        if self.factory is None:
            self.factory = sessionmaker(bind=self.engine)
        return self.factory()

## Create session "method"
create_session = SessionFactory()
