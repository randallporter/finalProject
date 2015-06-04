import os
from xml.dom import minidom
import logging

class Profile:

    def __init__(self, input_file_name):
        self.input_file_name = input_file_name
        self.profile_path = ".\\profiles\\"
        self.categories = {}
        self.categories_map = {}

        # No profile exists
        if not os.path.exists(self.profile_path + self.input_file_name):
            self.categories = {1: "apparel", 2: "automotive", 3: "bills", 4: "credit card payments",
                               5: "electronics", 6: "entertainment", 7: "gas", 8: "groceries", 9: "health",
                               10: "hobbies", 11: "home improvements", 12: "online shopping", 13: "other",
                               14: "pet care", 15: "restaurants", 16: "taxes", 17: "travel"}
        # Profile exists
        else:
            xml_document = minidom.parse(self.profile_path + self.input_file_name)
            # build categories dict
            cat_list = xml_document.getElementsByTagName('category')
            for cat in cat_list:
                self.categories[int(str(cat.attributes['id'].value))] = str(cat.attributes['name'].value)
            # build categories map which is dict of array values
            cat_map_list = xml_document.getElementsByTagName('categorymap')
            for cat_map in cat_map_list:
                cat_id = int(str(cat_map.attributes['id'].value))
                cat_ame = str(cat_map.attributes['name'].value)
                logging.debug(str(id) + "|||" + cat_ame)
                if cat_id not in self.categories_map:
                    self.categories_map.update({cat_id: []})
                self.categories_map[cat_id].append(cat_ame)

    def get_categories(self):
        return self.categories

    def get_categories_map(self):
        return self.categories_map

    def get_name(self):
        return self.input_file_name.split(".")[0]

    def export(self):
        with open(self.profile_path + self.input_file_name, "w+") as f:
            f.write("<data>")
            f.write("<categories>")
            for k, v in self.categories.items():
                f.write("<category id=\"" + str(k) + "\" name=\"" + v + "\"></category>")
            f.write("</categories>")

            f.write("<categoriesMap>")
            for k, v in self.categories_map.items():
                for array_item in v:
                    f.write("<categorymap id=\"" + str(k) + "\" name=\"" + array_item + "\"></categorymap>")
            f.write("</categoriesMap>")
            f.write("</data>")



