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
        with open("test1.csv","w+") as f1:
            f1.write("test,test,test")
        with open("test2.csv","w+") as f2:
            f2.write("test,test,test")
        with open("test2.csv","w+") as f3:
            f3.write("test,test,test")

        correctFileList = {1: "test1.csv", 2: "test2.csv", 3: "test3.csv"}

        self.assertEqual(correctFileList, get_csvs("."))

        for testFile in correctFileList.values(): os.remove(testFile)

    def test_find_no_csv(self):
        self.assertEqual({}, get_csvs("."))
