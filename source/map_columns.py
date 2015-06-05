from source.user_input import get_string, get_int, cls
from xml.dom import minidom
import os


class Mapping:
    def __init__(self, name, has_header=None, amount=None, date=None, memo=None, negative=None):
        self.mapping_path = ".\\mappings\\"
        self.mapping_ext = ".xml"
        self.name = name

        if not os.path.exists(self.mapping_path + self.name + self.mapping_ext):
            self.has_header = has_header
            self.amount_column_index = amount
            self.date_column_index = date
            self.memo_column_index = memo
            self.debit_as_negative = negative
        else:
            xml_document = minidom.parse(self.mapping_path + self.name + self.mapping_ext)
            x_map = xml_document.getElementsByTagName('mapping')[0]
            self.has_header = bool(x_map.attributes['hasHeader'].value)
            self.amount_column_index = int(x_map.attributes['amountIndex'].value)
            self.date_column_index = int(x_map.attributes['dateIndex'].value)
            self.memo_column_index = int(x_map.attributes['memoIndex'].value)
            self.debit_as_negative = bool(x_map.attributes['debitNegative'].value)

    def __eq__(self, other):
        return self.name == other.name \
            and self.has_header == other.has_header \
            and self.amount_column_index == other.amount_column_index \
            and self.date_column_index == other.date_column_index \
            and self.memo_column_index == other.memo_column_index \
            and self.debit_as_negative == other.debit_as_negative

    def export(self):
        if os.path.exists(self.mapping_path + self.name + self.mapping_ext):
            os.remove(self.mapping_path + self.name + self.mapping_ext)

        with open(self.mapping_path + self.name + self.mapping_ext, "w+") as f:
            f.write("<mapping")
            f.write(" name=\"" + self.name + "\"")
            f.write(" hasHeader=\"" + str(self.has_header) + "\"")
            f.write(" amountIndex=\"" + str(self.amount_column_index) + "\"")
            f.write(" dateIndex=\"" + str(self.date_column_index) + "\"")
            f.write(" memoIndex=\"" + str(self.memo_column_index) + "\"")
            f.write(" debitNegative=\"" + str(self.debit_as_negative) + "\"")
            f.write("></mapping>")


def display_row(row):
    index = 1
    for string in row:
        print str(index) + ". " + string
        index += 1


def get_has_headers():
    return get_string("Does the file have headers? Enter Y or N for yes or no") == "Y"


def get_columns():
    amount = get_int("Enter the column number corresponding to transaction amounts")
    date = get_int("Enter the column number corresponding to dates")
    memo = get_int("Enter the column number corresponding to memos")

    return [amount, date, memo]


def get_negative_withdrawals():
    return get_string("Does the file use negative values for withdrawals? Enter Y or N for yes or no") == "Y"


def map_columns(row, name):
    mapping = Mapping(name)
    # if has_headers is null no map already exists
    if mapping.has_header is None:
        display_row(row)
        has_header = get_has_headers()
        cls()
        display_row(row)
        mapping = get_columns()
        cls()
        display_row(row)
        negative = get_negative_withdrawals()
        cls()
        mapping = Mapping(name, has_header, mapping[0], mapping[1], mapping[2], negative)
    return mapping
