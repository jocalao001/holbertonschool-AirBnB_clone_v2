#!/usr/bin/python3
"""Module to test database storage"""


from models import storage
import MySQLdb
import unittest
import inspect
import io
import sys
import cmd
import shutil
import os
import console
import json

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

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.state import State

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

        def test_all_method(self):
            """Test for all method"""
            storage.save()
            exec_command(my_console, 'create State name="Cali"')
            self.db.commit()
            total = len(storage.all(State))
            total_con = len(json.loads(exec_command(my_console, "all State")))
            self.assertAlmostEqual(total, total_con)
            exec_command(my_console, 'create State name="Cali"')
            self.db.commit()
            total_con = len(json.loads(exec_command(my_console, "all State")))
            self.assertAlmostEqual(total_con, total + 1)

else:
    pass
