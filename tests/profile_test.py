from source.Profile import Profile
from unittest import TestCase
import os


class TestImport(TestCase):
    """
    """

    def test_create_new_profile(self):
        profile = Profile("John Jacob Jingle.xml")
        self.assertEqual(profile.get_name(), "John Jacob Jingle")
        test_categories = {1: "apparel", 2: "automotive", 3: "bills", 4: "credit card payments", 5: "electronics",
                           6: "entertainment", 7: "gas", 8: "groceries", 9: "health", 10: "hobbies", 11: "home improvements",
                           12: "online shopping", 13: "other", 14: "pet care", 15: "restaurants", 16: "taxes", 17: "travel"}
        self.assertEqual(profile.get_categories(), test_categories)
        self.assertEqual(profile.get_categories_map(), {})

    def test_create_and_export_existing_profile(self):
        test_dir = './profiles/'
        profile_name = "John.xml"
        setup_xml = "<data>" \
                    "<categories>" \
                    "<category id=\"1\" name=\"Beer\"></category>" \
                    "<category id=\"2\" name=\"Bread\"></category>" \
                    "</categories>" \
                    "<categoriesMap>" \
                    "<categorymap id=\"1\" name=\"safeway\"></categorymap>" \
                    "<categorymap id=\"1\" name=\"76\"></categorymap>" \
                    "<categorymap id=\"2\" name=\"fred-meyer\"></categorymap>" \
                    "<categorymap id=\"2\" name=\"wonder\"></categorymap>" \
                    "</categoriesMap>" \
                    "</data>"

        with open(test_dir + profile_name, "w+") as f:
            f.write(setup_xml)

        profile = Profile(profile_name)
        self.assertEqual(profile.get_name(), profile_name.split(".")[0])
        self.assertEqual(profile.get_categories(), {1: "Beer", 2: "Bread"})
        self.assertEqual(profile.get_categories_map(), {1: ["safeway", "76"], 2: ["fred-meyer", "wonder"]})

        profile.export()

        with open(test_dir + profile_name) as f:
            file_guts = f.read()

        self.assertEqual(file_guts, setup_xml)

        if os.path.exists(test_dir + profile_name):
            os.remove(test_dir + profile_name)




