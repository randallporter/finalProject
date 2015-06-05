import os

def prompt():
    raw_input("Press enter to continue . . . ")
    return


def get_int(input_string):
    return int(raw_input(input_string + ": "))


def get_string(input_string):
    return raw_input(input_string + ": ")


def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])