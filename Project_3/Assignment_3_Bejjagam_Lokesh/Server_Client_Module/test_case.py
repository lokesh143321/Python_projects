"""Test_case Module"""
import time
import unittest
from server_functions import server_func


class Test_cases(unittest.TestCase):
    """
    class Test_cases

    Attributes: none

    Methods:
        Individual test cases
    """
    def tearDown(self):
        time.sleep(1)
    def test_0_registration(self):
        server_obj = server_func()
        actual = server_obj.test_registration("register demotest 123")
        expected = "success"
        self.assertEqual(actual, expected)
    print(test_0_registration.__doc__)
    def test_1_login(self):
        server_obj = server_func()
        actual = server_obj.test_login("login demotest 123")
        expected = "success"
        self.assertEqual(actual, expected)
    print(test_1_login.__doc__)
    def test_2_command_list(self):
        server_obj = server_func()
        actual = server_obj.test_commands_list()
        expected = """***COMMANDS***\nCommand: change_folder <folder_Name>\nDescription: Used to
        move to the corresponding folder_Name\nCommand: list
        \nDescription: Used to print all the files and folders in the current directory\nCommand: read_file <file_Name>
        \nDescription: Used to read the contents of the file\nCommand: write_file <file_Name> <input_data>
        \nDescription: Used to write the <input_data> into the <file_Name>\nCommand: create_folder <folder_Name>\nDescription: Used to create a folder under the current directory
        \nCommand: commands\nDescription: Used to display the valid commands\nCommand: register <username> <password>\nDescription: Used to register a user\nCommand: login <username> <password>\nDescription: Used to login with registered valid user
        \nCommand: quit\nDescription: Used to disconnect from the server"""
        self.assertEqual(actual, expected)
    print(test_2_command_list.__doc__)
    def test_3_create_folder(self):
        server_obj = server_func()
        actual = server_obj.test_create_folder("create_folder test01")
        expected = "success"
        self.assertEqual(actual, expected)
    print(test_3_create_folder.__doc__)
    def test_4_change_folder(self):
        server_obj = server_func()
        actual = server_obj.test_change_folder("change_folder test01")
        expected = "success"
        self.assertEqual(actual, expected)
    print(test_4_change_folder.__doc__)
    def test_5_write_file(self):
        server_obj = server_func()
        actual = server_obj.test_write_file("write_file testdata.txt test data01")
        expected = "success"
        self.assertEqual(actual, expected)
    print(test_5_write_file.__doc__)
    def test_6_read_file(self):
        server_obj = server_func()
        actual = server_obj.test_read_file("read_file testdata.txt")
        expected = "success"
        self.assertEqual(actual, expected)
