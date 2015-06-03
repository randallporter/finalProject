from source.user_input import get_string, get_int

import os

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

class Mapping:
    def __init__(self, name, has_header, amount, date, memo, negative = True):
        self.name = name
        self.has_header = has_header
        self.amount_column_index = amount
        self.date_column_index = date
        self.memo_column_index = memo
        self.debit_as_negative = negative

def display_row(row):
    index = 1
    for string in row:
        print str(index) + ". " + string
        index += 1

def get_has_headers():
    return get_string("Does the file have headers? Enter Y or N for yes or no") == "Y"

def get_columns(row):
    amount = get_int("Enter the column number corresponding to transaction amounts")
    date = get_int("Enter the column number corresponding to dates")
    memo = get_int("Enter the column number corresponding to memos")

    return [amount, date, memo]
