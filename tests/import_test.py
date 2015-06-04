from unittest import TestCase
from source.importingFile import get_csvs, csv_to_dict_of_arrays
import os
from mock import patch
import datetime
import getpass
import random
import socket
import subprocess
import threading
import time
import logging


class TestImport(TestCase):
    """
    """

    def test_find_three_csv(self):
        self.test_dir = ".\\test_files\\"
        self.correct_file_list = ["test1.csv", "test2.csv", "test3.csv"]
        with patch("os.path.exists", return_value = True):
            with patch("os.listdir", return_value = ["test1.csv", "test2.csv", "test3.csv", "blah.txt", "fakefile"]):
                self.assertEqual(self.correct_file_list, sorted(get_csvs(self.test_dir)))

    def test_bad_path(self):
        with self.assertRaises(Exception):
            with patch("os.path.exists", return_value = False):
                get_csvs(".\\asdasdasdasd\\")

    def test_load_csvs(self):
        file_contents = {"test1.csv":"ya da,b lah,tr r\naa d6,4 345,a a",
                              "test2.csv":" ,,sdfsdf\n,a,qwerty"}
        expected_output = {"test1.csv":[["ya da","b lah", "tr r"], ["aa d6", "4 345", "a a"]],
                              "test2.csv":[[" ","", "sdfsdf"], ["", "a", "qwerty"]]}
        for file_name in file_contents.keys():
            with open(file_name, "w") as f:
                f.write(file_contents[file_name])

        result = csv_to_dict_of_arrays(file_contents.keys())
        print result
        self.assertEqual(result, expected_output)

        for file_name in file_contents.keys():
            os.remove(file_name)