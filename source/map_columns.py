from source.user_input import get_string, get_int

import os


def cls():
    os.system(['clear','cls'][os.name == 'nt'])


class Mapping:
    def __init__(self, name, has_header, amount, date, memo, negative):
        self.name = name
        self.has_header = has_header
        self.amount_column_index = amount
        self.date_column_index = date
        self.memo_column_index = memo
        self.debit_as_negative = negative

    def __eq__(self, other) :
        return self.name == other.name \
            and self.has_header == other.has_header \
            and self.amount_column_index == other.amount_column_index \
            and self.date_column_index == other.date_column_index \
            and self.memo_column_index == other.memo_column_index \
            and self.debit_as_negative == other.debit_as_negative


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


def get_bank_name():
    return get_string("Enter the name of the bank this file is from")


def map_columns(row):
    name = get_bank_name()
    display_row(row)
    has_header = get_has_headers()
    cls()
    display_row(row)
    mapping = get_columns()
    cls()
    display_row(row)
    negative = get_negative_withdrawals()
    cls()
    return Mapping(name, has_header, mapping[0], mapping[1], mapping[2], negative)
