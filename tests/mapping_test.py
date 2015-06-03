from unittest import TestCase
from source.Transaction import Transaction
import os
import datetime
import getpass
import random
import socket
import subprocess
import threading
import time
import logging


class TestMapper(TestCase):

    def setUp(self):
        self.test_trans = Transaction(amount=-8.99, date="2/8/2015 10:44 PM", memo="444500071733 LITTLE CAESARS 1593 159 ALOHA ORUS")

    def tearDown(self):
        pass

    def test_create_map(self):
        pass


