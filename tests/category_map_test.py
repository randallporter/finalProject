from unittest import TestCase
import source.map_categories
from source.Transaction import Transaction
from source.Profile import Profile
from io import BytesIO
from mock import patch
import difflib
import os


class TestMatching(TestCase):

    def test_get_highest_match_per_category(self):

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")
        fake_categories_map = {8: [["safeway 1", "Safeway 234", "Safeway A"],
                                   ["Fred Meyer", "Fred Meyer 1", "FredMeyer"]],
                               1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}

        result = source.map_categories.get_highest_match_per_category(fake_transaction, fake_categories_map)

        expected = {8: 82, 1: 27}

        self.assertEqual(result, expected)

    def test_compare_single_string(self):

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")
        fake_string = "Fred Meyer"

        result = source.map_categories.single_string_similarity(fake_transaction, fake_string)
        expected = int(difflib.SequenceMatcher(a=fake_transaction.memo.upper(), b=fake_string.upper()).ratio() * 100)

        self.assertEqual(result, expected)

    def test_compare_multiple_string(self):

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")
        fake_string_list = ["Fred Meyer", "Fred Meyer 1", "FredMeyer", "FrED 1 MEYER 110"]

        result = source.map_categories.multi_string_average_similarity(fake_transaction, fake_string_list)

        expected = 0

        for a in fake_string_list:
            expected += difflib.SequenceMatcher(a=fake_transaction.memo.upper(), b=a.upper()).ratio() * 100

        expected = int(expected / len(fake_string_list))

        self.assertEqual(result, expected)

    def test_get_match_per_string_array(self):

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")
        fake_string_lists = [["Fred Meyer", "Fred Meyer 1", "FredMeyer", "FrED 1 MEYER 110"],
                              ["safeway 1", "Safeway 234", "Safeway A"],
                              ["Home depot", "home depot asd", "homedepot"],
                              ["lowe's", "LOWES", "LOWES 12121"]]

        expected = [source.map_categories.multi_string_average_similarity(fake_transaction, fake_string_lists[0]),
                    source.map_categories.multi_string_average_similarity(fake_transaction, fake_string_lists[1]),
                    source.map_categories.multi_string_average_similarity(fake_transaction, fake_string_lists[2]),
                    source.map_categories.multi_string_average_similarity(fake_transaction, fake_string_lists[3])]

        result = source.map_categories.get_match_per_string_array(fake_transaction, fake_string_lists)

        self.assertEqual(expected, result)

    @patch('sys.stdout', new_callable=BytesIO)
    def test_display_max_for_each_category(self, mock_stdout):

        fake_categories_map = {8: [["safeway 1", "Safeway 234", "Safeway A"], ["Fred Meyer", "Fred Meyer 1", "FredMeyer"]],
                               1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}
        fake_category_names = {8: "groceries", 1: "home improvement"}

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")

        correct_output = "1. home improvement: 27%\n8. groceries: 82%\n"

        source.map_categories.display_max_per_category(fake_transaction, fake_categories_map, fake_category_names)

        self.assertEqual(mock_stdout.getvalue(), correct_output)

    @patch('sys.stdout', new_callable=BytesIO)
    def test_automatic_match(self, mock_stdout):

        fake_categories_map = {8: [["safeway 1", "Safeway 234", "Safeway A"], ["Fred Meyer", "Fred Meyer 1", "FredMeyer"]],
                               1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}
        fake_category_names = {8: "groceries", 1: "home improvement"}

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")

        expected = {8: [["safeway 1", "Safeway 234", "Safeway A"], ["Fred Meyer", "Fred Meyer 1", "FredMeyer", "FREDMEYER 123"]],
                               1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}

        fake_tolerance = 80

        source.map_categories.match_transaction_to_category(fake_transaction, fake_categories_map,
                                                            fake_category_names, fake_tolerance)

        expected_output = 'Mapped "' + fake_transaction.memo + '" to category "groceries" (82% match)\n'

        self.assertEqual(fake_categories_map, expected)
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        self.assertEqual(fake_transaction.categoryID, 8)

    @patch('sys.stdout', new_callable=BytesIO)
    def test_user_match(self, mock_stdout):

        fake_categories_map = {8: [["safeway 1", "Safeway 234", "Safeway A"], ["Fred Meyer", "Fred Meyer 1", "FredMeyer"]],
                               1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}
        fake_category_names = {8: "groceries", 1: "home improvement"}

        fake_transaction = Transaction("10.99", "11/02/1992 9:00", "Grocery Outlet 27")

        expected = {8: [["safeway 1", "Safeway 234", "Safeway A"], ["Fred Meyer", "Fred Meyer 1", "FredMeyer"], ["Grocery Outlet 27"]],
                               1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}

        fake_tolerance = 80

        with patch('__builtin__.raw_input', return_value="8") as mock_input:
            source.map_categories.match_transaction_to_category(fake_transaction, fake_categories_map, fake_category_names, fake_tolerance)
        mock_input.assert_called_with('\n Enter the category number that "' + fake_transaction.memo + '" fits into and press enter: ')

        expected_output = "1. home improvement: 35%\n8. groceries: 24%\n"
        expected_output_1 = 'Mapped "' + fake_transaction.memo + '" to category "groceries"\n'

        self.assertEqual(fake_categories_map, expected)
        self.assertEqual(fake_transaction.categoryID, 8)
        self.assertEqual(mock_stdout.getvalue(), expected_output + expected_output_1)