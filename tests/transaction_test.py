from unittest import TestCase
from source.Transaction import Transaction, map_data_to_transaction
from source.map_columns import Mapping


class TestTransaction(TestCase):

    def test_map_data_to_transaction(self):
        data = ["2/8/2015 10:44",
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
        correct_transaction = Transaction("-8.99", "2/8/2015 10:44",
                                          "444500071733 LITTLE CAESARS 1593 159ALOHA        ORUS")

        test_mapping = Mapping("First Tech FCU", True, 7, 1, 4, True)
        result = map_data_to_transaction(data, test_mapping)
        self.assertEqual(result, correct_transaction)
