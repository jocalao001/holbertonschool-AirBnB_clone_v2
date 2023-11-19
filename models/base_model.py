#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(
            String(60),
            default=lambda: str(uuid.uuid4()),
            primary_key=True,
            nullable=False,
        )
        created_at = Column(DateTime, default=datetime.now(), nullable=False)
        updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    else:

        def __init__(self, *args, **kwargs):
            """Instatntiates a new model"""
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            if kwargs:
                for k, v in kwargs.items():
                    if k == "__class__":
                        continue
                    if k == "id":
                        self.id = v
                    elif k == "created_at":
                        self.created_at = datetime.fromisoformat(v)
                    elif k == "updated_at":
                        self.updated_at = datetime.fromisoformat(v)
                    else:
                        setattr(self, k, v)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        di = self.__dict__
        di.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(cls, self.id, di)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({"__class__": (str(type(self)).split(".")[-1]).split("'")[0]})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Delete the current instance from the storage (models.storage)
        by calling the method delete"""
        from models import storage

        storage.delete()
