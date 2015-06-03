from unittest import TestCase
from mock import patch
import source.user_input

class TestUserInput(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_question_displayed(self):
        with patch('__builtin__.raw_input', return_value=None) as mock_input:
            source.user_input.prompt()

        mock_input.assert_called_with("Press enter to continue . . . ")

    def test_get_int(self):
        with patch('__builtin__.raw_input', return_value=5) as mock_input:
            self.assertEqual(source.user_input.get_int("Enter a number"), 5)

        mock_input.assert_called_with("Enter a number: ")

    def test_get_string(self):
        with patch('__builtin__.raw_input', return_value="Bob") as mock_input:
            self.assertEqual(source.user_input.get_string("Enter your name"), "Bob")

        mock_input.assert_called_with("Enter your name: ")