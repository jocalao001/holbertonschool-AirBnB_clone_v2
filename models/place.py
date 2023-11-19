#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Integer, Table
from sqlalchemy.orm import relationship
import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False,
        ),
        Column(
            "amenity_id", ForeignKey("amenities.id"), primary_key=True, nullable=False
        ),
    )

    class Place(BaseModel, Base):
        """State class"""

        __tablename__ = "places"
        name = Column(String(128), nullable=False)
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates="place_amenities",
            viewonly=False,
        )

else:

    class Place(BaseModel):
        """A place to stay"""

        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            from models.review import Review
            from models import storage

            rev = storage.all(Review)
            place = storage.all(Place)
            id_places = [v.id for v in place.values()]
            rev = [v for v in rev.values() if v.place_id in id_places]
            return rev

        @property
        def amenities(self):
            from models.review import Amenity

            amens = storage.all(Amenity)
            list_amens = [amen for amen in amens.values() if amen.id in amenity_ids]
            return list_amens

        @amenities.setter
        def amenities(self, obj):
            if obj.__class__.__name__ == "Amenity":
                amenity_ids.append(obj.id)
            else:
                pass
