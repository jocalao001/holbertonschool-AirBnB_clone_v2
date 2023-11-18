#!/usr/bin/python3
""" """
from models.place import Place
import os


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    import MySQLdb
    import unittest
    import inspect
    import io
    import sys
    import cmd
    import shutil
    import console

    """
        Backup console
    """
    if os.path.exists("copy_console.py"):
        shutil.copy("copy_console.py", "console.py")
    shutil.copy("console.py", "copy_console.py")

    """
        Updating console to remove "__main__"
    """
    with open("copy_console.py", "r") as file_i:
        console_lines = file_i.readlines()
        with open("console.py", "w") as file_o:
            in_main = False
            for line in console_lines:
                if "__main__" in line:
                    in_main = True
                elif in_main:
                    if "cmdloop" not in line:
                        file_o.write(line.lstrip("    "))
                else:
                    file_o.write(line)

    """
     Create console
    """
    console_obj = "HBNBCommand"
    for name, obj in inspect.getmembers(console):
        if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
            console_obj = obj

    my_console = console_obj(stdout=io.StringIO(), stdin=io.StringIO())
    my_console.use_rawinput = False

    """
     Exec command
    """

    def exec_command(my_console, the_command, last_lines=1):
        my_console.stdout = io.StringIO()
        real_stdout = sys.stdout
        sys.stdout = my_console.stdout
        my_console.onecmd(the_command)
        sys.stdout = real_stdout
        lines = my_console.stdout.getvalue().split("\n")
        return "\n".join(lines[(-1 * (last_lines + 1)) : -1])

    DB_CONFIG = {
        "host": "localhost",
        "user": "hbnb_test",
        "password": "hbnb_test_pwd",
        "db": "hbnb_test_db",
    }

    class TestPlace(unittest.TestCase):
        """Test cases for class Place"""

        def setUp(self):
            """Connect to the test database and create a cursor"""
            self.db = MySQLdb.connect(**DB_CONFIG)
            self.cursor = self.db.cursor()

        def tearDown(self):
            """Close the cursor and connection after the test"""
            self.cursor.close()
            self.db.close()

        def test_create_place(self):
            """Test for creating places"""
            # Create State
            state_id = exec_command(my_console, 'create State name="Utah"')
            self.db.commit()

            # Create City
            city_id = exec_command(
                my_console,
                f"""create City name="Delta"
                                      state_id="{state_id}" """,
            )
            self.db.commit()

            # Create User
            user_id = exec_command(
                my_console,
                f"""create User email="a@.com"
                                   password="apasswd" """,
            )
            self.db.commit()

            # Create Place
            place_id = exec_command(
                my_console,
                f"""create Place name="Los_Alamos"
                                    number_rooms=4 number_bathrooms=3
                                    max_guest=8 price_by_night=320
                                    latitude=23.1234 longitude=-23.1234
                                    user_id="{user_id}"
                                    city_id="{city_id}" """,
            )
            self.db.commit()

        def test_place_exist(self):
            """Test for checking if place name exist"""
            self.cursor.execute("SELECT name FROM places")
            names_1 = self.cursor.fetchall()
            name_exist = "Los Alamos" in [
                tup[0] for tup in names_1 if "Los Alamos" in tup
            ]
            self.assertTrue(name_exist)

        def test_type_name(self):
            """Test for checking typest"""
            self.cursor.execute("SELECT name FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), str)

        def test_type_number_rooms(self):
            """Test for checking typest"""
            self.cursor.execute("SELECT number_rooms FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), int)

        def test_number_baths_type(self):
            """Test for checking if number rooms exist"""
            self.cursor.execute("SELECT number_bathrooms FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), int)

        def test_max_guest_type(self):
            """Test for checking if number rooms exist"""
            self.cursor.execute("SELECT max_guest FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), int)

        def test_price_type(self):
            """Test for checking if number rooms exist"""
            self.cursor.execute("SELECT price_by_night FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), int)

        def test_user_id_type(self):
            """Test for checking if number rooms exist"""
            self.cursor.execute("SELECT user_id FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), str)

        def test_city_id_type(self):
            """Test for checking if number rooms exist"""
            self.cursor.execute("SELECT city_id FROM places")
            names_1 = self.cursor.fetchall()
            self.assertEqual(type(names_1[0][0]), str)

        def test_max_guest_exist(self):
            """Test for checking if max_guest exist"""
            self.cursor.execute("SELECT max_guest FROM places")
            names_1 = self.cursor.fetchall()
            name_exist = 8 in [tup[0] for tup in names_1 if 8 in tup]
            self.assertTrue(name_exist)

        def test_number_bath_exist(self):
            """Test for checking if number baths exist"""
            self.cursor.execute("SELECT number_bathrooms FROM places")
            names_1 = self.cursor.fetchall()
            name_exist = 3 in [tup[0] for tup in names_1 if 3 in tup]
            self.assertTrue(name_exist)

        def test_price_exist(self):
            """Test for checking if price exist"""
            self.cursor.execute("SELECT price_by_night FROM places")
            names_1 = self.cursor.fetchall()
            name_exist = 320 in [tup[0] for tup in names_1 if 320 in tup]
            self.assertTrue(name_exist)

        def test_latitude_exist(self):
            """Test for checking if latitude exist"""
            self.cursor.execute("SELECT latitude FROM places")
            names_1 = self.cursor.fetchall()
            name_exist = 23.1234 in [tup[0] for tup in names_1 if 23.1234 in tup]
            self.assertTrue(name_exist)

        def test_longitude_exist(self):
            """Test for checking if latitude exist"""
            self.cursor.execute("SELECT longitude FROM places")
            names_1 = self.cursor.fetchall()
            name_exist = -23.1234 in [tup[0] for tup in names_1 if -23.1234 in tup]
            self.assertTrue(name_exist)

else:
    from tests.test_models.test_base_model import test_basemodel

    class test_Place(test_basemodel):
        """ """

        def __init__(self, *args, **kwargs):
            """ """
            super().__init__(*args, **kwargs)
            self.name = "Place"
            self.value = Place

        def test_city_id(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.city_id), str)

        def test_user_id(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.user_id), str)

        def test_name(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.name), str)

        def test_description(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.description), str)

        def test_number_rooms(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.number_rooms), int)

        def test_number_bathrooms(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.number_bathrooms), int)

        def test_max_guest(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.max_guest), int)

        def test_price_by_night(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.price_by_night), int)

        def test_latitude(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.latitude), float)

        def test_longitude(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.latitude), float)

        def test_amenity_ids(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.amenity_ids), list)
