import os

def get_csvs(provided_path):
    file_list = []
    if os.path.exists(provided_path):
        for fileName in os.listdir(provided_path):
            if '.csv' in fileName:
                file_list.append(fileName)
    else:
        raise Exception(provided_path + " does not exist.")
    return file_list
