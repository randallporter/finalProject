from unittest import TestCase
from source.Transaction import Transaction, map_data_to_transaction, transaction_list_to_csv
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

    def test_transactions_to_csv(self):
        fake_transactions = [Transaction("1.23", "1/1/2011", "freddy's", categoryID=1),
                             Transaction("1.10", "2/2/2012", "safeway", categoryID=1),
                             Transaction("44.00", "3/3/2013", "binco's", categoryID=2),
                             Transaction("22.00", "4/4/2014", "macy's", categoryID=2),
                             Transaction("23.00", "5/5/2015", "union 76", categoryID=3)]
        fake_category_names = {1: "groceries", 2: "apparel", 3: "gas"}

        result = transaction_list_to_csv(fake_transactions, fake_category_names)

        expected = "1/1/2011,1.23,freddy's,groceries\n2/2/2012,1.10,safeway,groceries\n" \
                   "3/3/2013,44.00,binco's,apparel\n4/4/2014,22.00,macy's,apparel\n5/5/2015,23.00,union 76,gas\n"

        self.assertEqual(result, expected)