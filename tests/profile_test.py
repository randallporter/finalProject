from source.Profile import Profile
from source.Profile import get_input_name
from unittest import TestCase
import os
from mock import patch


class TestProfile(TestCase):
    """
    """
    def setUp(self):
        self.test_dir = '.\\profiles\\'
        self.profile_name = "John"
        self.profile_name_ext = ".xml"

    def tearDown(self):
        if os.path.exists(self.test_dir + self.profile_name + self.profile_name_ext):
            os.remove(self.test_dir + self.profile_name + self.profile_name_ext)

    def test_create_new_profile(self):
        # ENTER NAME
        with patch('__builtin__.raw_input', return_value="John Jacob Jingle") as mock_input:
            name_given = get_input_name()
            self.assertEqual("John Jacob Jingle", name_given)
            mock_input.assert_called_with("Enter either your Profile name or a new profile name: ")

        profile = Profile("John Jacob Jingle")
        self.assertEqual(profile.get_name(), "John Jacob Jingle")
        test_categories = {1: "apparel", 2: "automotive", 3: "bills", 4: "credit card payments", 5: "electronics",
                           6: "entertainment", 7: "gas", 8: "groceries", 9: "health", 10: "hobbies", 11: "home improvements",
                           12: "online shopping", 13: "other", 14: "pet care", 15: "restaurants", 16: "taxes", 17: "travel"}
        self.assertEqual(profile.get_categories(), test_categories)
        self.assertEqual(profile.get_categories_map(), {})

        # ENTER CATEGORIES TO DELETE
        test_categories = profile.print_categories()
        with patch('__builtin__.raw_input', return_value="1,10,12") as mock_input:
            profile.get_categories_to_delete()
            mock_input.assert_called_with(test_categories + "Enter the indexes of the categories you do not want, "
                                          "separated by a comma (ex: 1,2,3) or type 'skip': ")
        test_categories = {2: "automotive", 3: "bills", 4: "credit card payments", 5: "electronics",
                           6: "entertainment", 7: "gas", 8: "groceries", 9: "health", 11: "home improvements",
                           13: "other", 14: "pet care", 15: "restaurants", 16: "taxes", 17: "travel"}
        self.assertEqual(profile.get_categories(), test_categories)

        # ENTER CATEGORIES TO ADD
        with patch('__builtin__.raw_input', return_value="costco,garden") as mock_input:
            profile.get_categories_to_add()
            mock_input.assert_called_with("Enter the names of any new categories, "
                                          "separated by a comma (ex: shoes,gas,out to eat) or type 'skip': ")
        test_categories = {2: "automotive", 3: "bills", 4: "credit card payments", 5: "electronics",
                           6: "entertainment", 7: "gas", 8: "groceries", 9: "health", 11: "home improvements",
                           13: "other", 14: "pet care", 15: "restaurants", 16: "taxes", 17: "travel",
                           18: "costco", 19: "garden"}
        self.assertEqual(profile.get_categories(), test_categories)

        # SELECT FILES
        with patch('__builtin__.raw_input', side_effect=["skip", "bank2", "bank1"]) as mock_input:
            self.test_dir = ".\\test_files\\"
            self.correct_file_list = {"test3.csv": "", "test2.csv": "", "test1.csv": ""}
            with patch("os.path.exists", return_value=True):
                with patch("os.listdir", return_value=["test1.csv", "test2.csv", "test3.csv", "blah.txt", "fakefile"]):
                    profile.get_csvs(self.test_dir)
                    self.assertEqual(self.correct_file_list, profile.file_name_bank_map)
            profile.get_file_banks()
            self.assertEqual({"test2.csv": "bank2", "test1.csv": "bank1"},
                             profile.file_name_bank_map)
            mock_input.assert_any_call("Enter the name of the bank this file is from or type 'skip' you do not wish to "
                                       "use that file: ")
            self.assertEqual(mock_input.call_count, 3)

        # Ask upper_tolerance
        with patch('__builtin__.raw_input', return_value="75") as mock_input:
            profile.get_input_tolerance()
            self.assertEqual(75, profile.upper_tolerance)
            mock_input.assert_called_with("Enter a number between 0 and 100 to represent the percentage match you"
                                          " would like for the system to auto categorize the transaction: ")

    def test_create_and_export_existing_profile(self):
        setup_xml = "<data>" \
                    "<categories>" \
                    "<category id=\"1\" name=\"Beer\"></category>" \
                    "<category id=\"2\" name=\"Bread\"></category>" \
                    "</categories>" \
                    "<categoriesMap>" \
                    "<categorymap id=\"1\" index=\"0\" name=\"safeway\"></categorymap>" \
                    "<categorymap id=\"1\" index=\"0\" name=\"safeway drugs\"></categorymap>" \
                    "<categorymap id=\"1\" index=\"1\" name=\"albertsons\"></categorymap>" \
                    "<categorymap id=\"2\" index=\"0\" name=\"fred-meyer\"></categorymap>" \
                    "<categorymap id=\"2\" index=\"1\" name=\"wonder\"></categorymap>" \
                    "</categoriesMap>" \
                    "</data>"

        with open(self.test_dir + self.profile_name + self.profile_name_ext, "w+") as f:
            f.write(setup_xml)

        profile = Profile(self.profile_name)
        self.assertEqual(profile.get_name(), self.profile_name)
        self.assertEqual(profile.get_categories(), {1: "Beer", 2: "Bread"})
        self.assertEqual(profile.get_categories_map(), {1: [["safeway", "safeway drugs"], ["albertsons"]],
                                                        2: [["fred-meyer"], ["wonder"]]})

        profile.export()

        with open(self.test_dir + self.profile_name + self.profile_name_ext) as f:
            file_guts = f.read()

        self.assertEqual(file_guts, setup_xml)

    # TODO export transactions

