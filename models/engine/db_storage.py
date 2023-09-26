#!/usr/bin/python3
"""New engine DBStorage"""
# to get enviromental variables
from os import environ

# to create the engine
from sqlalchemy import create_engine

# create_engine syntaxis: [dialect]+[driver]://[username]:[password]@[host]:[port]/[database]
# to delete all tables if we are in a test enviroment
# to create all tables based on engine
from models.base_model import Base

# retrieving all the classes
# to create the current db session
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import session


class DBStorage:
    """New class that represents an storage engine and has the
    following attributes"""

    __engine = None
    __session = None

    # public instance method
    def __init__(self):
        """This method creates the engine, the engine must be linked
        to the MySQL database and user created in previus tasks
        hbnb_dev and hbnb_dev_db"""
        # creating engine using the enviromental variables (retrieving values vía enviromental variables)
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                environ.get("HBNB_MYSQL_USER"),
                environ.get("HBNB_MYSQL_PWD"),
                environ.get("HBNB_MYSQL_HOST"),
                environ.get("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        # avoiding te accidental elimination of data in a production or dev enviroment
        if environ.get("HBNB_ENV") == "test":
            Base.metadata.drop_all()

    def all(self, cls=None):
        """Retrieves objects from the database based on the class name provided.
        Returns a dictionary just like Filestorage"""
        classes = [State, City, User, Place, Review, Amenity]

        # if cls not in classes:
        #    print("** Class doesn't exist **")

        # empty dict to store the objects
        objects_dict = {}

        # make sure that we are in a database session
        if self.__session is None:
            print("** no session established **")
            return {}

        # quering all types of objects when no class is passed
        if cls is None:
            for clase in classes:
                # query all types
                cls_objs = self.__session.query(clase).all()
                for ob in cls_objs:
                    del ob._sa_instance_state  # doesn't work
                    # clean_ob = object.to_dict() doesn't work
                    # add the objecto to the dictionary
                    # ob.pop("_sa_instance_state", None) doesn't work
                    objects_dict[f"{type(cls).__name__}.{ob.id}"] = ob
        else:
            # if there is a specific class query it
            cls_objs = self.__session.query(cls).all()
            # add the obj of the specified class to the dictionary
            for ob in cls_objs:
                del ob._sa_instance_state  # doesn't work
                # clean_ob = object.to_dict() doesn't work
                # add the objecto to the dictionary
                # ob.pop("_sa_instance_state", None) doesn't work
                objects_dict[f"{type(cls).__name__}.{ob.id}"] = ob

        # return the dictionary
        return objects_dict

    def new(self, obj):
        """This method will add the object to the current database session
        (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """This method will save the changes to te objects in the current
        session so this will persist the objects in the database"""
        self.__session.commit()

    def delete(self, obj):
        """This method will delete an object from the current session.
        This method also marks the object for deletion in the database
        when a commit() is performed"""
        self.__session.delete(obj)

    def reload(self):
        """Creates all the tables in the database and creates the current
        database session"""
        # Create all tables in the database session
        Base.metadata.create_all(self.__engine)
        # creating the current session using and bind to the engine
        # Set the parameter expire_on_commit to False
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # we need to make sure that our session is thread-safe
        # and make sure that every subprocess works with it's own
        # session instance.
        session.Session = scoped_session(session_factory)
        # make sure the session is secure
        self.__session = session.Session()

    def close(self):
        """Closes the current session"""
        self.__session.close()
