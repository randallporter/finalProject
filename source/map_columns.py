from source.user_input import get_string

def display_row(row):
    index = 1
    for string in row:
        print str(index) + ". " + string
        index += 1

def get_has_headers():
    return get_string("Does the file have headers? Enter Y or N for yes or no") == "Y"
