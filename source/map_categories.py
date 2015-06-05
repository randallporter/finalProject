import difflib


def single_string_similarity(transaction, input_string):
    return int(difflib.SequenceMatcher(a=transaction.memo.upper(), b=input_string.upper()).ratio() * 100)


def multi_string_average_similarity(transaction, input_string_array):
    total = 0
    for memo in input_string_array:
        total += single_string_similarity(transaction, memo)

    return total / len(input_string_array)


def get_match_per_string_array(transaction, input_string_array_array):
    returned_list = []
    for string_list in input_string_array_array:
        returned_list.append(multi_string_average_similarity(transaction, string_list))
    return returned_list


def get_highest_match_per_category(transaction, categories_map):
    returned_dict = {}
    for category in categories_map.keys():
        returned_dict[category] = max(get_match_per_string_array(transaction, categories_map[category]))
    return returned_dict

def display_max_per_category(transaction, categories_map, category_names):

    matches = get_highest_match_per_category(transaction, categories_map)

    for key in sorted(categories_map.keys()):
        print str(key) + ". " + category_names[key] + ": " + str(matches[key]) + "%"