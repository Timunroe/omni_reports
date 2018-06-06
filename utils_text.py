import pdftotext
import re

# ===== PDF ==========


def process_pdf(f):
    # READ PDF, EXTRACT TEXT
    # memory_file = open('DailySpec.pdf','rb')
    memory_file = open(f, 'rb')
    pdf = pdftotext.PDF(memory_file)
    memory_file.close()

    # Iterate over all the pages
    pdf_text = ""
    for page in pdf:
        pdf_text += page

    # returns a multi-lne string
    return pdf_text

# ===== TEXT PARSING ==========


def find_between(ms, first, last):
    # print("==========\nIn function 'find_between\n==========")
    # takes a multiline string 'ms', extracts a substring
    # based on marker strings 'first', 'last'
    try:
        start = ms.index(first) + len(first)
        end = ms.index(last, start)
        return ms[start:end]
    except ValueError:
        return ""


def lines(ms):
    # print("==========\nIn function 'lines\n==========")
    # takes multiline string 'ms' and creates list of non-empty strings(lines)
    # while removing ALL whitespace characters (space, tab, newline, return, formfeed)
    # and replacing with single spaces
    # ALSO removes leading and trailing whitespace
    temp = [" ".join(line.strip().split()) for line in ms.splitlines()]
    return [line for line in temp if line != '']


def line_modify(s, list_remove, list_subs):
    # print("==========\nIn function 'line_modify\n==========")
    # print(f"Value of 's' passed in:\n{s}")
    # Modify string passed in as 's',
    # removing items in the list 'list_remove'
    # and replacing strings with replacements as found in list of tuples 'list_subs'
    for item in list_remove:
        s = s.replace(item, '')
    for index, item in enumerate(list_subs):
        s = s.replace(item[0], item[1])

    # Remove the period from rank numbers eg 1.
    # We couldn't remove periods before because the process was indiscriminant
    # Here we can be specific with regex

    new_line = re.sub(r"^(\d{1,2})\. ", "\\1 ", s)

    # Handle cases where a line may have may have multiple words
    # We need to fill those spaces so we later we can split the line on spaces
    # NOTE: This may be faulty logic in future
    new_line = re.sub(r"([a-zA-Z]) (\(?[a-zA-Z])", "\\1-\\2", new_line)
    # print(new_line)

    # Turn each 'line' into a list of strings, delimited by spaces
    new_list = new_line.split()
    # HERE IS A GOOD PLACE TO CONVERT EACH STRING OF DIGITS TO A NUMBER!
    # and convert URLs to asset ID's
    mod_list = []
    for item in new_list:
        # print(item)
        if bool(re.search(r'/\d{7}-', item)):
            asset_id = re.sub(r"https.*/(\d{7})-.*", "\\1", item)
            # print(f"Asset id: {asset_id}")
            mod_list.append(int(asset_id))
        elif bool(re.search(r'^\d+$', item)):
            mod_list.append(int(item))
        elif bool(re.search(r'\d\.\d', item)):
            mod_list.append(float(item))
        else:
            mod_list.append(item)
    # pp.pprint(mod_list)
    return mod_list


def line_objectify(l_line, t_keys):
    # where list l_line = ['value, 'value', 'value']
    # and list of tuples t_keys = [(key, index in l_line), (key, index in l_line)]
    # Example: l_line = ["this", "that", "bob"] and t_keys = [("first", 0), ("second", 1), ("name", 2)]
    # results in a dict {"first": "this", "second": "that", "name": "bob"}
    # print(l_line)
    # print("t_keys list:")
    # print(t_keys)
    return {k[0]: l_line[k[1]] for k in t_keys}


def merge_lists(l_primary, l_secondary, s_match_key):
    # Takes two list of dicts, with each dict in first list having (usually) one matching key-pair
    # with a dict in the second list, and combines them based on the matching key-pair
    # Note: sometimes this won't be the case, for example, list of referring domains might
    # change from week to week. Will return None if no match
    # Returns one list

    # temporary holding list
    new_list = []

    # for each dict in list, find the dict in other list with same key-value pair
    for obj in l_primary:
        # we know the key, now get this loop's value
        match_value = obj[s_match_key]
        # get the index of the matching dict in the other list
        idex = next((i for i, d in enumerate(l_secondary) if match_value in d.values()), None)
        # print("index of " + obj[s_match_key] + ' is ' + str(idex))
        if idex is not None:
            # new Python 3.5 syntax for merging dictionaries
            new_dic = {**obj, **l_secondary[idex]}
            # put this new list of dicts in the holding list
            new_list.append(new_dic)
    return new_list


def find_dict_in_list(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return None


def find_index_of_dict_in_list(l, key, value):
    for i, dic in enumerate(l):
        if dic[key] == value:
            return i
    return None


def reduce_list_of_dicts(l, key_same, key_sum):
    # this finds all dicts with a same key, and adds that key's values
    # NOTE: key_sum can be a list ['a', 'b'] in that case all a's summed, all b's summed
    # Yields new list with only 1 instance dict with that key with all values summed
    # useful, for example, if there are multiple page view listings with same asset ID
    # Can't compare first item in list, so add it
    new_list = [l[0]]
    # Start list with second item ...
    for item in l[1:]:
        flag = False
        for i, dic in enumerate(new_list):
            if dic[key_same] == item[key_same]:
                idex = i
                flag = True
                if isinstance(key_sum, list):
                    for x in key_sum:
                        new_list[idex][x] += item[x]
                else:
                    new_list[idex][key_sum] += item[key_sum]
        if not flag:
            new_list.append(item)
    return new_list
