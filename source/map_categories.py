import difflib
import source.user_input
import logging


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

def match_transaction_to_category(transaction, categories_map, category_names, tolerance):

    all_matches = get_highest_match_per_category(transaction, categories_map)

    max_match = key_with_max_val(all_matches)

    if all_matches[max_match] >= tolerance:
        matches_array = get_match_per_string_array(transaction, categories_map[max_match])
        if transaction.memo not in categories_map[max_match][matches_array.index(max(matches_array))]:
            categories_map[max_match][matches_array.index(max(matches_array))].append(transaction.memo)
        transaction.categoryID = max_match
        print 'Mapped "' + transaction.memo + '" to category "' + category_names[max_match] + '" (' + str(all_matches[max(all_matches)]) + '% match)'
    else:
        display_max_per_category(transaction, categories_map, category_names)
        category = source.user_input.get_int('\n Enter the category number that "' + transaction.memo + '" fits into and press enter')
        logging.debug('Mapped "' + transaction.memo + '" to category "' + category_names[category] + '" (' + str(category) + ')')
        categories_map[category].append([transaction.memo])
        transaction.categoryID = category
        print 'Mapped "' + transaction.memo + '" to category "' + category_names[category] + '"'

def match_transactions_to_categories(transactions, categories_map, category_names, tolerance):
    for transaction in transactions:
        match_transaction_to_category(transaction, categories_map, category_names, tolerance)


def key_with_max_val(dict):
    """ a) create a list of the dict's keys and values;
    b) return the key with the max value"""
    values=list(dict.values())
    keys=list(dict.keys())
    return keys[values.index(max(values))]