import os

def get_csvs(provided_path, files):
    file_list = []
    index = 0
    if os.path.exists(provided_path):
        for fileName in os.listdir(provided_path):
            if '.csv' in fileName:
                file_list.append(fileName)
            index += 1
    else:
        raise Exception(provided_path + " does not exist.")
    if index != files:
        raise Exception("only " + str(index) + " files in directory")
    return file_list
