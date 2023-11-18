#!/usr/bin/python3
""" """
from models.review import Review
import os


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    import MySQLdb
    from models.place import Place
    from models import storage
    import unittest
    import inspect
    import io
    import sys
    import cmd
    import shutil
    import console
    import datetime

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

    class TestReview(unittest.TestCase):
        """Test cases for Review class"""

        def setUp(self):
            """Connect to the test database and create a cursor"""
            self.db = MySQLdb.connect(**DB_CONFIG)
            self.cursor = self.db.cursor()

        def tearDown(self):
            """Close the cursor and connection after the test"""
            self.cursor.close()
            self.db.close()

        def test_create_reviews(self):
            """Test for creating reviews"""
            # Create State
            state_id = exec_command(my_console, 'create State name="Texas"')
            self.db.commit()

            # Create City
            city_id = exec_command(
                my_console,
                f"""create City
                                   state_id="{state_id}" name="Alpine" """,
            )
            self.db.commit()

            # Create User
            user_id = exec_command(
                my_console,
                f"""create User email="a@x.com"
                                   password="apasswd" """,
            )
            self.db.commit()

            # Create Places
            place_id = exec_command(
                my_console,
                f"""create Place user_id="{user_id}"
                                    city_id="{city_id}"
                                    name="Central_Park" """,
            )
            self.db.commit()

            # Create Review
            review_id = exec_command(
                my_console,
                f"""create Review
                                     place_id="{place_id}"
                                     user_id="{user_id}"
                                     text="It_is_awesome" """,
            )
            self.db.commit()

        def test_review_exist(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT text FROM reviews")
            texts = self.cursor.fetchall()
            text_exist = "It is awesome" in [
                tup[0] for tup in texts if "It is awesome" in tup
            ]
            self.assertTrue(text_exist)

        def test_type_name(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT text FROM reviews")
            texts = self.cursor.fetchall()
            self.assertTrue(type(texts[0][0]), str)

        def test_type_user_id(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT user_id FROM reviews")
            texts = self.cursor.fetchall()
            self.assertTrue(type(texts[0][0]), str)

        def test_type_place_id(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT place_id FROM reviews")
            texts = self.cursor.fetchall()
            self.assertTrue(type(texts[0][0]), str)

        def test_type_id(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT id FROM reviews")
            texts = self.cursor.fetchall()
            self.assertTrue(type(texts[0][0]), str)

        def test_type_created_at(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT created_at FROM reviews")
            texts = self.cursor.fetchall()
            self.assertTrue(type(texts[0][0]), datetime.datetime)

        def test_type_updated_at(self):
            """Test for checking if review text exist"""
            self.cursor.execute("SELECT updated_at FROM reviews")
            texts = self.cursor.fetchall()
            self.assertTrue(type(texts[0][0]), datetime.datetime)

else:
    from tests.test_models.test_base_model import test_basemodel

    class test_review(test_basemodel):
        """ """

        def __init__(self, *args, **kwargs):
            """ """
            super().__init__(*args, **kwargs)
            self.name = "Review"
            self.value = Review

        def test_place_id(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.place_id), str)

        def test_user_id(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.user_id), str)

        def test_text(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.text), str)
