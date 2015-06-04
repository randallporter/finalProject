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

def csv_to_dict_of_arrays(file_names):
    data = {}
    for file_name in file_names:
        with open(file_name) as f:
            data[file_name] = []
            for line in f.readlines():
                try:
                    split_strings = line.split(",")
                    stripped_strings = []
                    for string in split_strings:
                        stripped_strings.append(string.rstrip('\n'))
                    data[file_name].append(stripped_strings)
                except:
                    pass
    return data
