from unittest import TestCase
from source.importingFile import get_csvs
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
