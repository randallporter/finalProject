from source.Profile import Profile
from source.Profile import csv_to_dict_of_arrays, get_input_name
from source.map_columns import map_columns
from source.Transaction import map_data_to_transaction
from source.map_categories import match_transactions_to_categories
from unittest import TestCase
import os
from mock import patch
import source


if __name__ == "__main__":
    name_given = get_input_name()
    profile = Profile(name_given)
    profile.get_categories_to_delete()
    profile.get_categories_to_add()
    profile.get_csvs()
    profile.get_file_banks()
    # Fill transaction_list based on file_name_bank_map and the name of the map
    for k, v in csv_to_dict_of_arrays(profile.file_name_bank_map.keys()).items():
        mapping = map_columns(v[0], profile.file_name_bank_map[k])
        if mapping.has_header:
            v.remove(v[0])
        for csv_line in v:
            profile.transaction_list.append(map_data_to_transaction(csv_line, mapping))
        mapping.export()
    profile.get_input_tolerance()
    match_transactions_to_categories(transactions=profile.transaction_list,
                                     categories_map=profile.categories_map,
                                     category_names=profile.categories,
                                     tolerance=profile.upper_tolerance)
    profile.export()
