#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import os


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    class State(BaseModel, Base):
        """ State class """

        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
                                "City",
                                backref='state',
                                cascade="all, delete-orphan"
                                )

else:
    class State(BaseModel):
        """ State class """
        name = ""

        @property
        def cities(self):
            from models import storage
            from models.city import City
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
