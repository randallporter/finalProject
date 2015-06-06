from unittest import TestCase
import source.Profile
import source.Transaction
import time
import os

class PerfTests(TestCase):

    def tearDown(self):
        csv_filename = ".\\profiles\\deleteme export.csv"
        xml_filename = ".\\profiles\\deleteme.xml"

        if os.path.exists(csv_filename):
            os.remove(csv_filename)

        if os.path.exists(xml_filename):
            os.remove(xml_filename)

    def test_large_import(self):

        t = "Performance.csv"

        test_file_names = []

        for a in range(100):
            test_file_names.append(t)

        start = time.clock()
        throwaway = source.Profile.csv_to_dict_of_arrays(test_file_names)
        end = time.clock() - start

        self.assertLess(end, 5)

    def test_transactions_to_csv(self):

        fake_transaction = source.Transaction.Transaction("12.99", "1/1/2011", "asiudhsaiudiusadh as iludh sia uhd", categoryID=1)
        fake_cat_names = {1: "asohuidoiusahd"}

        fake_transaction_list = []

        for a in range(20000):
            fake_transaction_list.append(fake_transaction)

        start = time.clock()
        source.Transaction.transaction_list_to_csv(fake_transaction_list, fake_cat_names)
        end = time.clock() - start

        self.assertLess(end, 5)

        fake_profile = source.Profile.Profile("deleteme")

        fake_profile.transaction_list = fake_transaction_list

        start = time.clock()
        fake_profile.export()
        end = time.clock() - start

        self.assertLess(end, 5)