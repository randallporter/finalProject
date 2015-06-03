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

    def test_find_three_csv(self):
        test_dir = './tests/'

        with open(test_dir + "test1.csv", "w+") as f1:
            f1.write("test,test,test")
        with open(test_dir + "test2.csv", "w+") as f2:
            f2.write("test,test,test")
        with open(test_dir + "test3.csv", "w+") as f3:
            f3.write("test,test,test")

        correct_file_list = ["test1.csv", "test2.csv", "test3.csv"]

        self.assertTrue(correct_file_list <= get_csvs(test_dir))

        for testFile in correct_file_list:
            os.remove(test_dir + testFile)

    def test_find_no_csv(self):
        self.assertEqual([], get_csvs('./tests/'))

    def test_bad_path(self):
        self.assertEqual([], get_csvs('./testsklhygugvyuugbjgk/'))
