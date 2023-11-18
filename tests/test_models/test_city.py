#!/usr/bin/python3
""" """
from models.city import City
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

    class TestDBStorage(unittest.TestCase):
        """Test cases for database storage"""

        def setUp(self):
            """Connect to the test database and create a cursor"""
            self.db = MySQLdb.connect(**DB_CONFIG)
            self.cursor = self.db.cursor()

        def tearDown(self):
            """Close the cursor and connection after the test"""
            self.cursor.close()
            self.db.close()

        def test_create_city(self):
            """Test for creating city"""
            state_id_3 = exec_command(my_console, 'create State name="Colorado"')
            self.db.commit()
            city_id_1 = exec_command(
                my_console,
                f"""create City
                                     name=\"Denver\"
                                     state_id=\"{state_id_3}\" """,
            )
            self.db.commit()
            self.cursor.execute("SELECT COUNT(id) AS count_1 FROM cities")
            count_1 = self.cursor.fetchall()

            self.cursor.execute("SELECT state_id FROM cities")
            rows_1 = self.cursor.fetchall()
            state_ids = state_id_3 in [tup[0] for tup in rows_1 if tup[0]]
            self.assertTrue(state_ids)

        def test_type_name_state(self):
            """Comment"""
            self.cursor.execute("SELECT name FROM cities")
            rows_1 = self.cursor.fetchall()
            self.assertEqual(type(rows_1[0][0]), str)

        def test_type_id_state(self):
            """Comment"""
            self.cursor.execute("SELECT id FROM cities")
            rows_1 = self.cursor.fetchall()
            self.assertEqual(type(rows_1[0][0]), str)

        def test_type_state_id_state(self):
            """Comment"""
            self.cursor.execute("SELECT state_id FROM cities")
            rows_1 = self.cursor.fetchall()
            self.assertEqual(type(rows_1[0][0]), str)

        def test_city_exist(self):
            """Test for checking if state name exist"""
            self.cursor.execute("SELECT name FROM cities")
            names = self.cursor.fetchall()
            name_exist = "Denver" in [tup[0] for tup in names if "Denver" in tup]
            self.assertTrue(name_exist)

else:
    from tests.test_models.test_base_model import test_basemodel

    class test_City(test_basemodel):
        """ """

        def __init__(self, *args, **kwargs):
            """ """
            super().__init__(*args, **kwargs)
            self.name = "City"
            self.value = City

        def test_state_id(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.state_id), str)

        def test_name(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.name), str)
