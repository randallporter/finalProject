from unittest import TestCase
import source.map_categories
from source.Transaction import Transaction
from source.Profile import Profile
from io import BytesIO
from mock import patch
import difflib
import os


class TestMatching(TestCase):

    @patch('sys.stdout', new_callable=BytesIO)
    def test_display_matches(self, mock_stdout):

        fake_transaction = Transaction("2.49", "11/02/1991 8:00", "FREDMEYER 123")

        with patch("os.path.exists", return_value = False):
            fake_profile = Profile("yada")

        fake_profile.categories_map = {8: [["safeway 1", "Safeway 234", "Safeway A"], ["Fred Meyer", "Fred Meyer 1", "FredMeyer"]],
                                       1: [["Home depot", "home depot asd", "homedepot"], ["lowe's", "LOWES", "LOWES 12121"]]}

        #matches = {}
        #for a in fake_profile.categories_map:


        #source.map_categories.display_matches(fake_profile, fake_transaction)

        #self.correct_output = "
        #self.assertEqual(mock_stdout.getvalue(), self.correct_output)
