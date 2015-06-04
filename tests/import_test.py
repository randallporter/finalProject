from unittest import TestCase
from source.importingFile import get_csvs
import os
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

    def setUp(self):
        self.test_dir = ".\\test_files\\"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        with open(self.test_dir + "test1.csv", "w+") as f1:
            f1.write("test,test,test")
        with open(self.test_dir + "test2.csv", "w+") as f2:
            f2.write("test,test,test")
        with open(self.test_dir + "test3.csv", "w+") as f3:
            f3.write("test,test,test")

        self.correct_file_list = ["test1.csv", "test2.csv", "test3.csv"]

    def tearDown(self):
        for testFile in self.correct_file_list:
            os.remove(self.test_dir + testFile)
        os.rmdir(self.test_dir)

    def test_find_three_csv(self):
        self.assertEqual(self.correct_file_list, sorted(get_csvs(self.test_dir)))

    def test_find_no_csv(self):
        empty_dir = ".\\nothing_here\\"
        if not os.path.exists(empty_dir):
            os.makedirs(empty_dir)
        self.assertEqual([], get_csvs(empty_dir))
        os.rmdir(empty_dir)

    def test_bad_path(self):
        with self.assertRaises(Exception):
            get_csvs(".\\asdasdasdasd\\")
