from unittest import TestCase
from source.Profile import csv_to_dict_of_arrays
import os
from mock import patch


class TestImport(TestCase):
    """
    """

    def test_load_csvs(self):
        file_contents = {"test1.csv":"ya da,b lah,tr r\naa d6,4 345,a a",
                              "test2.csv":" ,,sdfsdf\n,a,qwerty"}
        expected_output = {"test1.csv":[["ya da","b lah", "tr r"], ["aa d6", "4 345", "a a"]],
                              "test2.csv":[[" ","", "sdfsdf"], ["", "a", "qwerty"]]}
        for file_name in file_contents.keys():
            with open(file_name, "w") as f:
                f.write(file_contents[file_name])

        result = csv_to_dict_of_arrays(file_contents.keys())
        self.assertEqual(result, expected_output)

        for file_name in file_contents.keys():
            os.remove(file_name)