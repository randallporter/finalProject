from unittest import TestCase
import source.map_columns
from io import BytesIO
from mock import patch

class TestMapper(TestCase):

    def setUp(self):
        self.row = ["2/8/2015 10:44",
                    "ID2992",
                    "POS Transaction",
                    "444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS",
                    "POS Transaction 444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS",
                    "",
                    "-8.99",
                    "",
                    "417.72",
                    "2/8/2015 0:00",
                    ""]

    def tearDown(self):
        pass

    @patch('sys.stdout', new_callable=BytesIO)
    def test_display_row(self, mock_stdout):
        source.map_columns.display_row(self.row)
        self.correct_output = "1. 2/8/2015 10:44\n2. ID2992\n3. POS Transaction\n4. 444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS\n5. POS Transaction 444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS\n6. \n7. -8.99\n8. \n9. 417.72\n10. 2/8/2015 0:00\n11. \n"
        self.assertEqual(mock_stdout.getvalue(), self.correct_output)

    def test_header(self):
        with patch('__builtin__.raw_input', return_value="Y") as mock_input:
            self.assertTrue(source.map_columns.get_has_headers())
        mock_input.assert_called_with("Does the file have headers? Enter Y or N for yes or no: ")

        with patch('__builtin__.raw_input', return_value="N"):
            self.assertFalse(source.map_columns.get_has_headers())

    def test_selection(self):
        # amount: 7, date: 1, memo: 4
        with patch('__builtin__.raw_input', side_effect=["7", "1", "4"]) as mock_input:
            self.assertEqual(source.map_columns.get_columns(), [7, 1, 4])
        mock_input.assert_any_call("Enter the column number corresponding to transaction amounts: ")
        mock_input.assert_any_call("Enter the column number corresponding to dates: ")
        mock_input.assert_any_call("Enter the column number corresponding to memos: ")
        self.assertEqual(mock_input.call_count, 3)

    def test_negative_amount(self):
        with patch('__builtin__.raw_input', return_value="Y") as mock_input:
            self.assertTrue(source.map_columns.get_negative_withdrawals())
        mock_input.assert_called_with("Does the file use negative values for withdrawals? Enter Y or N for yes or no: ")

        with patch('__builtin__.raw_input', return_value="N"):
            self.assertFalse(source.map_columns.get_negative_withdrawals())

    def test_bank_name(self):
        with patch('__builtin__.raw_input', return_value="First Tech FCU") as mock_input:
            self.assertEqual(source.map_columns.get_bank_name(), "First Tech FCU")
        mock_input.assert_called_with("Enter the name of the bank this file is from: ")

    def test_create_mapping(self):
        test_mapping = source.map_columns.Mapping("First Tech FCU", True, 7, 1, 4, True)
        with patch('sys.stdout'):
            with patch('__builtin__.raw_input', side_effect=["First Tech FCU", "Y", "7", "1", "4", "Y"]):
                self.assertEqual(source.map_columns.map_columns(self.row), test_mapping)