import os
from xml.dom import minidom
import logging
from source.user_input import get_string, get_int


class Profile:

    def __init__(self, input_file_name):
        self.name = input_file_name
        self.profile_path = ".\\profiles\\"
        self.profile_ext = ".xml"
        self.categories = {}            # dictionary
        self.categories_map = {}        # dictionary of an array of arrays
        self.transaction_list = []      # array of transactions
        self.file_name_bank_map = {}    # dictionary with file name as k and bank name from user as v
        self.upper_tolerance = None
        self.transaction_list = []
        self.upper_tolerance = 80   # 80%

        # No profile exists
        if not os.path.exists(self.profile_path + self.name + self.profile_ext):
            self.categories = {1: "apparel", 2: "automotive", 3: "bills", 4: "credit card payments",
                               5: "electronics", 6: "entertainment", 7: "gas", 8: "groceries", 9: "health",
                               10: "hobbies", 11: "home improvements", 12: "online shopping", 13: "other",
                               14: "pet care", 15: "restaurants", 16: "taxes", 17: "travel"}
        # Profile exists
        else:
            xml_document = minidom.parse(self.profile_path + self.name + self.profile_ext)
            # build categories dict
            cat_list = xml_document.getElementsByTagName('category')
            for cat in cat_list:
                self.categories[int(str(cat.attributes['id'].value))] = str(cat.attributes['name'].value)
            # build categories map which is dict of array values
            cat_map_list = xml_document.getElementsByTagName('categorymap')
            for cat_map in cat_map_list:
                cat_id = int(str(cat_map.attributes['id'].value))
                cat_name = str(cat_map.attributes['name'].value)
                cat_idx = int(str(cat_map.attributes['index'].value))
                logging.debug(str(id) + "|||" + cat_name)
                if cat_id not in self.categories_map:
                    self.categories_map.update({cat_id: [[]]})
                if len(self.categories_map[cat_id]) <= cat_idx:
                    self.categories_map[cat_id].append([cat_name])
                else:
                    self.categories_map[cat_id][cat_idx].append(cat_name)

    def get_categories(self):
        return self.categories

    def get_categories_map(self):
        return self.categories_map

    def get_name(self):
        return self.name

    def export(self):
        if os.path.exists(self.profile_path + self.name + self.profile_ext):
            os.remove(self.profile_path + self.name + self.profile_ext)

        with open(self.profile_path + self.name + self.profile_ext, "w+") as f:
            f.write("<data>")
            f.write("<categories>")
            for k, v in self.categories.items():
                f.write("<category id=\"" + str(k) + "\" name=\"" + v + "\"></category>")
            f.write("</categories>")

            f.write("<categoriesMap>")
            for k, v in self.categories_map.items():
                i = 0
                for array_of_arrays in v:
                    for array_item in array_of_arrays:
                        f.write("<categorymap id=\"" + str(k) + "\" index=\"" + str(i) + "\" name=\"" + array_item + "\"></categorymap>")
                    i += 1
            f.write("</categoriesMap>")
            f.write("</data>")

    def print_categories(self):
        return_str = ""
        for k, v in self.categories.items():
            return_str += str(k) + " : " + v + "\n"
        return return_str

    def get_categories_to_delete(self):
        user_input = get_string(self.print_categories() + "Enter the indexes of the categories you do not want, "
                           "separated by a comma (ex: 1,2,3) or type 'skip'")
        user_input = user_input.split(",")
        for num in user_input:
            self.categories.pop(int(num))

    def get_categories_to_add(self):
        user_input = get_string("Enter the names of any new categories, "
                                "separated by a comma (ex: shoes,gas,out to eat) or type 'skip'")
        user_input = user_input.split(",")
        max_index = 0
        for idx in self.categories:
            max_index = idx
        for cat in user_input:
            max_index += 1
            self.categories.update({max_index: cat})

    def get_csvs(self, provided_path=".\\"):
        if os.path.exists(provided_path):
            for fileName in os.listdir(provided_path):
                if '.csv' in fileName:
                    self.file_name_bank_map.update({fileName: ""})

    def get_file_banks(self):
        delete_me = []
        for a_file in self.file_name_bank_map:
            user_input = get_string("Enter the name of the bank this file is from "
                                    "or type 'skip' you do not wish to use that file")
            if user_input != 'skip':
                self.file_name_bank_map[a_file] = user_input
            else:
                delete_me.append(a_file)
        for item in delete_me:
            self.file_name_bank_map.pop(item)


# NON CLASS HELPER FUNCTIONS


def csv_to_dict_of_arrays(file_names):
    data = {}
    for file_name in file_names:
        with open(file_name) as f:
            data[file_name] = []
            for line in f.readlines():
                try:
                    split_strings = line.split(",")
                    stripped_strings = []
                    for string in split_strings:
                        stripped_strings.append(string.rstrip('\n'))
                    data[file_name].append(stripped_strings)
                except:
                    pass
    return data


def get_input_name():
    return get_string("Enter either your Profile name or a new profile name")



