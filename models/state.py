#!/usr/bin/python3
""" State Module for HBNB project """
# now inherits also from Base
from models.base_model import BaseModel, Base

# importing column ans string for table attributes
from sqlalchemy import Column, String

# for relationship
from models.city import City
from sqlalchemy.orm import relationship

# Handling "dbstorage" and "filestorage" cases
from os import environ


class State(BaseModel, Base):
    """State class
    update: now will have new attributes to link to
    a MySQL table"""

    # when using "dbstorage"
    # if environ.get('HBNB_TYPE_STORAGE') == 'db':
    # new class attribute
    __tablename__ = "states"
    # class attribute changed
    name = Column(String(128), nullable=False)
    # for dbstorage relationship
    cities = relationship("City", backref="state", cascade="delete")

    # when using another type storage
    # the the enviromental variable is not implemented yet but is on top of the
    # project requirements
    if environ.get("HBNB_TYPE_STORAGE") != "db":
        # getter attribute when filestorage is used instead of dbstorage
        @property
        def cities(self):
            """Getter attribute that returns a list of city instances
            update: this method encapsules the logic of how to get
            instances of City related to a State"""
            # storage variableimported
            from models import storage

            # implement an empty list
            city_list = []
            # iterate through the City instances
            for city in storage.all(City).values():
                # in the previous task we update the state_id (class attribute)
                if city.state_id == self.id:
                    # Add cities that are related to state (current) to the list
                    city_list.append(city)
            # return that list
            return city_list
