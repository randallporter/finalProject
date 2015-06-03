import os

def get_csvs(provided_path):
    file_list = {}
    index = 1
    for fileName in os.listdir(provided_path):
        if '.csv' in fileName:
            file_list[index] = fileName
    return file_list