import os

def get_csvs(provided_path):
    file_list = {}
    if os.path.exists(provided_path):
        index = 1
        for fileName in os.listdir(provided_path):
            if '.csv' in fileName:
                file_list[index] = fileName
                index += 1
    return file_list