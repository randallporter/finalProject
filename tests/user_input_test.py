from unittest import TestCase
from mock import patch, Mock
from io import StringIO
import source.user_input
import os
import datetime
import getpass
import random
import socket
import subprocess
import threading
import time
import logging


class TestUserInput(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def question_displayed(self):
        raw_input = Mock(return_value=None)
        user_input.prompt("Please press enter . . . ")
        raw_input.assert_called_with("Please press enter . . . ")

    def get_int_test(self):
        raw_input = Mock(return_value=5)
        self.assertEqual(user_input.get_int("Enter a number"), 5)
        raw_input.assert_called_with("Enter a number: ")

    def get_string_test(self):
        raw_input = Mock(return_value="Bob")
        self.assertEqual(user_input.get_int("Enter your name"), "Bob")
        raw_input.assert_called_with("Enter your name: ")