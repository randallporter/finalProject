from unittest import TestCase
import source.map_columns
from io import BytesIO
from mock import patch
import os


class TestMapper(TestCase):

    def setUp(self):
        self.mapping_dir = '.\\mappings\\'
        self.mapping_name = "US BANK"
        self.mapping_ext = ".xml"
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
        if os.path.exists(self.mapping_dir + self.mapping_name + self.mapping_ext):
            os.remove(self.mapping_dir + self.mapping_name + self.mapping_ext)

    @patch('sys.stdout', new_callable=BytesIO)
    def test_display_row(self, mock_stdout):
        source.map_columns.display_row(self.row)
        self.correct_output = "1. 2/8/2015 10:44\n2. ID2992\n3. POS Transaction\n" \
                              "4. 444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS\n" \
                              "5. POS Transaction 444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS\n" \
                              "6. \n7. -8.99\n8. \n9. 417.72\n10. 2/8/2015 0:00\n11. \n"
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

    def test_create_mapping_not_exist(self):
        test_mapping = source.map_columns.Mapping("First Tech FCU", True, 7, 1, 4, True)
        with patch('sys.stdout'):
            with patch('__builtin__.raw_input', side_effect=["Y", "7", "1", "4", "Y"]):
                self.assertEqual(source.map_columns.map_columns(self.row, "First Tech FCU"), test_mapping)

    def test_create_mapping_from_file(self):
        setup_xml = "<mapping name=\"US BANK\" hasHeader=\"True\" amountIndex=\"1\" " \
                    "dateIndex=\"2\" memoIndex=\"3\" debitNegative=\"True\">" \
                    "</mapping>"

        with open(self.mapping_dir + self.mapping_name + self.mapping_ext, "w+") as f:
            f.write(setup_xml)

        mapping = source.map_columns.Mapping(self.mapping_name)

        self.assertEqual(mapping.name, self.mapping_name)
        self.assertEqual(mapping.has_header, True)
        self.assertEqual(mapping.amount_column_index, 1)
        self.assertEqual(mapping.date_column_index, 2)
        self.assertEqual(mapping.memo_column_index, 3)
        self.assertEqual(mapping.debit_as_negative, True)

        mapping.export()

        with open(self.mapping_dir + self.mapping_name + self.mapping_ext) as f:
            file_guts = f.read()

        self.assertEqual(file_guts, setup_xml)