#!/usr/bin/python3
""" """
from models.user import User
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

    class TestUser(unittest.TestCase):
        """Test cases for User class"""

        def setUp(self):
            """Connect to the test database and create a cursor"""
            self.db = MySQLdb.connect(**DB_CONFIG)
            self.cursor = self.db.cursor()

        def tearDown(self):
            """Close the cursor and connection after the test"""
            self.cursor.close()
            self.db.close()

        def test_create_user(self):
            """Test for creating users"""
            # Create State
            state_id = exec_command(my_console, 'create State name="Albama"')
            self.db.commit()

            # Create City
            city_id = exec_command(
                my_console,
                f"""create City
                                   state_id="{state_id}" name="Las_Vegas" """,
            )
            self.db.commit()

            # Create User
            user_id = exec_command(
                my_console,
                f"""create User email="fake@mail.com"
                                   password="fakepasswd" first_name="Lolo"
                                   last_name="Fernandez" """,
            )
            self.db.commit()

        def test_users_exist(self):
            """Test for checking if email exist"""
            self.cursor.execute("SELECT email FROM users")
            emails = self.cursor.fetchall()
            email_exist = "fake@mail.com" in [
                tup[0] for tup in emails if "fake@mail.com" in tup
            ]
            self.assertTrue(email_exist)

        def test_type_name(self):
            """Test for checking types"""
            self.cursor.execute("SELECT email FROM users")
            emails = self.cursor.fetchall()
            self.assertEqual(type(emails[0][0]), str)

        def test_type_password(self):
            """Test for checking types"""
            self.cursor.execute("SELECT password FROM users")
            emails = self.cursor.fetchall()
            self.assertEqual(type(emails[0][0]), str)

        def test_first_name_exist(self):
            """Test for checking if first name exist"""
            self.cursor.execute("SELECT first_name FROM users")
            first_names = self.cursor.fetchall()
            name_exist = "Lolo" in [tup[0] for tup in first_names if "Lolo" in tup]
            self.assertTrue(name_exist)

        def test_password_exist(self):
            """Test for checking if password exist"""
            self.cursor.execute("SELECT password FROM users")
            emails = self.cursor.fetchall()
            email_exist = "fakepasswd" in [
                tup[0] for tup in emails if "fakepasswd" in tup
            ]
            self.assertTrue(email_exist)

        def test_last_name_exist(self):
            """Test for checking if last name exist"""
            self.cursor.execute("SELECT last_name FROM users")
            emails = self.cursor.fetchall()
            email_exist = "Fernandez" in [
                tup[0] for tup in emails if "Fernandez" in tup
            ]
            self.assertTrue(email_exist)

else:
    from tests.test_models.test_base_model import test_basemodel

    class test_User(test_basemodel):
        """ """

        def __init__(self, *args, **kwargs):
            """ """
            super().__init__(*args, **kwargs)
            self.name = "User"
            self.value = User

        def test_first_name(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.first_name), str)

        def test_last_name(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.last_name), str)

        def test_email(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.email), str)

        def test_password(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.password), str)
