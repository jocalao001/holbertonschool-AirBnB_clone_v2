#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import models
from os import path
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return FileStorage.__objects
        else:
            temp_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    temp_dict[key] = value
            return temp_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.to_dict()['__class__'] + '.' + obj.id
        self.all().update({key: obj})

    def save(self):
        """Saves storage dictionary to file"""

        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f, indent=2, sort_keys=True)

    def reload(self):
        """Loads storage dictionary from file"""
        file_path = self.__file_path
        temp_dict = {}
        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

        if path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                temp_dict = json.load(f)

                for key, value in temp_dict.items():
                    extract_cls_name = value["__class__"]
                    check_cls_in_var = classes[extract_cls_name]
                    simple_instance = check_cls_in_var(**value)
                    self.all()[key] = simple_instance
                    # self.__objects[key] = simple_instance
                    
    def delete(self, obj=None):
        """This method deletes an object if it is passed
        otherwise returns"""
        if obj is None:
            # print("** command requires an obj to delete **")
            return
        else:
            for key, value in self.__objects.items():
                if value == obj:
                    del self.__objects[key]
                    break
    
    def close(self):
        """This method deserialices the json file to objects
        by calling the reload() method"""
        self.reload()
