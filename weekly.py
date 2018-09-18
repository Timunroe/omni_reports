import pdftotext
import requests
from bs4 import BeautifulSoup
import re
import pprint
import time
import json
import pyperclip

# TODO
# implement drop script in automator that calls script with arument of PDF dropped on it
# from PDF file name, read the day report is for, and what report method should be performed
# before outputting, save to json file with file date, rename PDF and move to 'done' folder
# make sure the final json has all the items and calculations needed, so outputting is
# straightforward

pp = pprint.PrettyPrinter(indent=2)

# GENERATE DAILY REPORT

# Stage 1 - process text from PDF, list of dicts
# [
#   section :[ {}, {}, {} ]
#   section :[ {}, {}, {} ]
#   section :[ {}, {}, {} ]
# ]

# Stage 2 - refine into object structure
# { metric: {
#    {xxx} : {}
# }

# get rid of rank, always sort by ... some value? usually page views

# VARIABLES LEGEND
# ms - multiline string, s - shorter string, line - longer string
# l - list, d - dict, t-tuple, k - key, v - value

# CONFIG
# holds settings necessary for parsing text
config = {
    "site": "spec",
    "pdf_name": "pdfs_new/Weekly.pdf",
    "sections": [
        {
            "name": "summary LW",
            "filter_lines": "number-comma",
            "trim": [3, None],
            "remove": [',', '%', 'Spent', 'Weekly'],
            "subs": [
                ['Average', 'Avg'],
                ['Signup Clicks', 'Signups'],
                [' Media / Email', '-email'],
            ],
            "keys": [
                # tuples where [0] is field name, [1] is field position
                ('metric', 0),
                ('value', 1),
            ],
            "markers": {
                "start": "Summary last week",
                "end": "Summary 3 mos"
            }
        },
        {
            "name": "summary L90",
            "filter_lines": "number-comma",
            "trim": [3, -3],
            "remove": [',', '%', 'Spent', 'Weekly'],
            "subs": [
                ['Average', 'Avg'],
                ['Signup Clicks', 'Signups'],
                [' Media / Email', '-email'],
            ],
            "keys": [
                ('metric', 0),
                ('value_l90', 1),
            ],
            "markers": {
                "start": "Summary 3 mos",
                "end": "PageViews compare"
            }
        },
        {
            "name": "Referring domains LW",
            "filter_lines": "percent",
            "trim": [3, -4],
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                ('domain', 1),
                ('pv', 2)
            ],
            "markers": {
                "start": "Ref Domains LW",
                "end": "Ref Domains L90"
            },
        },
        {
            "name": "Referring domains L90",
            "filter_lines": "percent",
            "trim": [3, -4],
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                ('domain', 1),
                ('pv_l90', 2)
            ],
            "markers": {
                "start": "Ref Domains L90",
                "end": "Tco top stories lw"
            },
        },
        # {
        #     "name": "Spec top stories",
        #     "filter_lines": "percent",
        #     "remove": [',', '%'],
        #     "targets": [],
        #     "subs": [],
        #     "keys": [
        #         ('asset', 1),
        #         ('pv', 2),
        #         ('%', 3)
        #     ],
        #     "markers": {
        #         "start": "Top Asset ID yesterday",
        #         "end": "Durham Top Asset ID ys"
        #     },
        # },
        # {
        #     "name": "Durham top stories",
        #     "filter_lines": "percent",
        #     "remove": [',', '%'],
        #     "targets": [],
        #     "subs": [],
        #     "keys": [
        #         ('asset', 1),
        #         ('pv', 2),
        #         ('%', 3)
        #     ],
        #     "markers": {
        #         "start": "Durham Top Asset ID ys",
        #         "end": "York Top Asset ID ys"
        #     },
        # },
        # {
        #     "name": "York top stories",
        #     "filter_lines": "percent",
        #     "remove": [',', '%'],
        #     "targets": [],
        #     "subs": [],
        #     "keys": [
        #         ('asset', 1),
        #         ('pv', 2),
        #         ('%', 3)
        #     ],
        #     "markers": {
        #         "start": "York Top Asset ID ys",
        #         "end": "Halton Top Asset ID ys"
        #     },
        # },
        # {
        #     "name": "Halton top stories",
        #     "filter_lines": "percent",
        #     "remove": [',', '%'],
        #     "targets": [],
        #     "subs": [],
        #     "keys": [
        #         ('asset', 1),
        #         ('pv', 2),
        #         ('%', 3)
        #     ],
        #     "markers": {
        #         "start": "Halton Top Asset ID ys",
        #         "end": "FB top stories ys"
        #     },
        # },
        {
            "name": "Facebook top stories",
            "filter_lines": "percent",
            "trim": [4, -3],
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                ('rank', 0),
                ('asset', 1),
                ('pv', 2),
                ('%', 3)
            ],
            "markers": {
                "start": "FB top stories lw",
                "end": "Most Popular Site Sections"
            },
        },
        {
            "name": "Twitter top stories",
            "filter_lines": "percent",
            "trim": [4, -3],
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                ('rank', 0),
                ('asset', 1),
                ('pv', 2),
                ('%', 3)
            ],
            "markers": {
                "start": "Tco top stories lw",
                "end": "FB top stories lw"
            },
        },
        {
            "name": "Device types LW",
            "filter_lines": "percent",
            "trim": [3, -4],
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                ('rank', 0),
                ('name', 1),
                ('pv', 2),
                ('%', 3)
            ],
            "markers": {
                "start": "Device Type last week",
                "end": " Device Type L90"
            },
        },
        {
            "name": "Device types L90",
            "filter_lines": "percent",
            "trim": [3, -4],
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                ('name', 1),
                ('pv_l90', 2),
                ('%_l90', 3)
            ],
            "markers": {
                "start": "Device Type L90",
                "end": "Ref Domains LW"
            },
        }
    ]
}


def parse_section(config, ms):
    # takes multiline string and extracts chunk based on markers in config's sections
    # then cleans the section of unwanted spaces
    # then turns into list of strings (lines)
    staging = {}
    # List to hold each section's text ready to become 'data'
    # allows us to see if parsing has worked
    # eg { 'section' : [ ['aa, '], }
    # print(config['sections'])
    for item in config['sections']:
        # print("Item name is: " + item['name'])
        # multi-step process returns list of strings from a big string
        # based on markers from 'config'
        # see comments in functions 'line' and 'find_between'
        # print("Marker start is: " + item['markers']['start'])
        clean_lines = lines(find_between(ms, item['markers']['start'], item['markers']['end']))
        print("Clean lines: ", clean_lines)

        # trim section from front, end based on 'trim' list of ints
        # ASSUMPTION: content we want will always be contiguous run of lines
        if item['trim']:
            clean_lines = clean_lines[item['trim'][0]:item['trim'][1]]

        # Tweak each line to remove or replace as noted in config:
        # each line comes back a list of strings
        # print("Matched lines:")
        # pp.pprint(matched_lines)
        # print("")

        modified_lines = [line_modify(line, item['remove'], item['subs']) for line in clean_lines]
        # print("Modified lines:")
        # pp.pprint(modified_lines)
        # print("")
        # Turn each line into dict with keys based on config['keys']
        objectified_lines = [line_objectify(line, item['keys']) for line in modified_lines]

        # Add all this text to the holding list 'staging'
        # grouped under the section name
        new_dict_key = item['name']
        new_dict_value = objectified_lines
        # new_dict = {new_dict_key: new_dict_value}
        # staging.append(new_dict)
        staging[new_dict_key] = new_dict_value

    return staging


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


# [ UTLITY FUNCTIONS ]--------------


def process_pdf(f):
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


def find_between(ms, first, last):
    # takes a multiline string 'ms', extracts a substring
    # based on marker strings 'first', 'last'
    try:
        start = ms.index(first) + len(first)
        end = ms.index(last, start)
        return ms[start:end]
    except ValueError:
        return ""


def lines(ms):
    # takes multiline string 'ms' and creates list of non-empty strings(lines)
    # while removing ALL whitespace characters (space, tab, newline, return, formfeed)
    # and replacing with single spaces
    # ALSO removes leading and trailing whitespace
    # should really have error trapping here
    # temp = [" ".join(line.strip().split()) for line in ms.splitlines() if line != '']
    temp = [" ".join(line.strip().split()) for line in ms.splitlines()]
    return [line for line in temp if line != '']


def line_modify(s, list_remove, list_subs):
    # Modify string passed in as 's',
    # removing items in the list 'list_remove'
    # and replacing strings in the list 'list_targets' with
    # strings in the the list 'list_replacements'
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

    # Turn each 'line' into a list of strings, delimited by spaces
    new_list = new_line.split()
    # HERE IS A GOOD PLACE TO CONVERT EACH STRING OF DIGITS TO A NUMBER!
    mod_list = []
    for item in new_list:
        if bool(re.search(r'^\d+$', item)):
            mod_list.append(int(item))
        elif bool(re.search(r'\d\.\d', item)):
            mod_list.append(float(item))
        else:
            mod_list.append(item)
    # pp.pprint(mod_list)
    return mod_list


def line_objectify(l_line, t_keys):
    # where l_line = ['value, 'value', 'value']
    # and t_keys = [(key, index in l_line), (key, index in l_line)]
    # takes in a list of strings, list of tuples
    # creates a dict from strings l_line
    # with keys from t_keys and values from l_line with index from t_keys
    # print("Line list supplied to line_objectify")
    # print(l_line)
    # print("t_keys list:")
    # print(t_keys)
    return {k[0]: l_line[k[1]] for k in t_keys}


def diff(new, old, kind=None):
    # takes in numbers
    # kinds: none (just subtraction), % is (new-old)/old, %90 (new-(old/90)/(old/90))
    # returns a formatted string
    if kind == '%90':
        result = ((new - (old / 90)) / (old / 90))
        result = "{:+.1%}".format(result)
    else:
        result = new - old
        result = "{:+.1}".format(result)
    return result


def percent(partial, total):
    # takes in numbers
    # returns formatted string
    result = (partial / total)
    result = "{:.1%}".format(result)
    return result


def find_dict_in_list(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return None


def output_summary(l):
    # l - list of dicts with same keys
    # s - holding string to return
    # diff_visits = diff(item['v'], item['v_l90'])
    # diff_shares = ''
    # diff_clicks = ''
    # spec_stats = [item for item in l if item["name"] == "Spec"]
    stats = [item for item in l]
    stats = stats[0]
    pv = stats['pv']
    pv_l90 = stats['pv_l90']
    uv = stats['uv']
    v = stats['v']
    v_l90 = stats['v_l90']

    s = '\n'
    s += '===================================================\n'
    s += 'SUMMARY: Page views, Unique visitors (UV), (V)isits\n'
    s += '===================================================\n'
    s += 'WEB       | Page      vs   |  PV/   | Visits   PV/\n'
    s += 'SITES     | Views     MA   |  UV    | vs MA    V\n'
    s += '---------------------------+----------------------\n'
    for item in l:
        if item['name'] == 'Metroland':
            item['name'] = "R of M"
            pv = "{:,}".format(item['pv'] - pv)
            diff_pv = diff((item['pv'] - pv), (item['pv_l90'] - pv_l90), '%90')
            pv_uv = "{:.3}".format((item['pv'] - pv) / (item['uv'] - uv))
            diff_v = diff(item['v'], (item['v_l90'] - v_l90), '%90')
            pv_v = "{:.3}".format((item['pv'] - pv) / (item['v'] - v))
        else:
            pv = "{:,}".format(item['pv'])
            diff_pv = diff(item['pv'], item['pv_l90'], '%90')
            pv_uv = "{:.3}".format(item['pv'] / item['uv'])
            diff_v = diff(item['v'], item['v_l90'], '%90')
            pv_v = "{:.3}".format(item['pv'] / item['v'])

        s += f"{item['name'].ljust(10)} {pv.rjust(7)}  {diff_pv.rjust(6)} |  {pv_uv.ljust(4, '0')}  |"
        s += f" {diff_v.rjust(6)}  {pv_v.ljust(4, '0')}\n"
        s += '---------------------------+-----------------------\n'
    s += 'MA = moving average = avg of last 90 days\n'
    s += 'R of M = Metroland minus Spectator stats\n'
    s += '==================================================\n'
    return s  # just a blank line


def output_devices(l):
    # print("list to output section")
    # pp.pprint(l)
    s = '\n'
    s += '=============================================\n'
    s += 'DEVICE     | % of     | Page    | vs 90-day  \n'
    s += 'TYPE       | total PV | views   | average  \n'
    s += '---------------------------------------------\n'
    for item in l:
        name = item['name'].replace('-', ' ').replace('Other', 'Desktop').replace(' Phone', '')
        pv = "{:,}".format(item['pv'])
        diff_per = diff(item['pv'], item['pv_l90'], '%90')

        s += f"{item['rank']}. {name.ljust(8)} {str(item['%']).rjust(7)}   {pv.rjust(9)}"
        s += f"   {diff_per.rjust(5)}\n"
    s += '---------------------------------------------\n'

    return s  # just a blank line


def output_referrers(l):
    # need to add up all values of keys pv, pv_l90
    # for every dict that has some form of 'google'
    # in key domain
    # then remove all those dicts except one
    # and change the pv, pv_190 values to the sums

    # total page views, from data['summary']
    tpv = find_dict_in_list(data['summary'], 'name', 'Spec')['pv']
    pv = 0
    pv_l90 = 0
    purge_index_list = []
    for index, d in enumerate(l):
        if 'google' in d['domain']:
            purge_index_list.append(index)
            d['domain'] = 'google'
            pv += int(d['pv'])
            pv_l90 += int(d['pv_l90'])

    # Creates a new list based on an item in list 'l' not having
    # an index value in list 'purge_index_list'
    reduced_list = [v for i, v in enumerate(l) if i not in purge_index_list[1:]]
    reduced_list[purge_index_list[0]]['pv'] = pv
    reduced_list[purge_index_list[0]]['pv_l90'] = pv_l90
    # sort list based on value in key pv
    # pp.pprint(l)
    sorted_list = sorted(reduced_list, key=lambda d: int(d['pv']), reverse=True)
    # pp.pprint(sorted_list)
    # NOW list l is ready to use
    s = '\n'
    s += '=============================================\n'
    s += 'TRAFFIC     | % of     | Page    | vs 90-day  \n'
    s += 'REFERRERS   | total PV | views   | average  \n'
    s += '---------------------------------------------\n'

    for i, item in enumerate(sorted_list[:5]):
        name = item['domain'].replace('/Bookmarked', '').replace('.com', '').replace('t.co', 'twitter')
        pv = "{:,}".format(item['pv'])
        pv_percent = percent(item['pv'], tpv)
        diff_per = diff(item['pv'], item['pv_l90'], '%90')
        s += f"{i + 1}. {name.ljust(9)} {pv_percent.rjust(7)}   {pv.rjust(9)}  {diff_per.rjust(7)}\n"
    s += '---------------------------------------------\n'

    return s


def output_top_stories(l, s_name):
    s = '\n'
    s += '===========================================================================================\n'
    s += f'{s_name.ljust(73)}| Page  | %\n'
    s += 'TOP STORIES                                                              | views | of PV\n'
    s += '-------------------------------------------------------------------------------------------\n'
    # remove items that don't have an asset number
    new_list = [item for item in l if bool(re.search(r'(\d{7}|\d{4})', item['asset']))][:5]
    for i, item in enumerate(new_list):
        story = item['asset'].replace('https://www.thespec.com/', '').replace('-story', '').replace('http://3downnation.com', '3Down')
        story = (story[:69]) if len(story) > 69 else story
        pv = "{:,}".format(item['pv'])
        percent = str(item['%'])
        s += f"{i+1}. {story.ljust(69)} {pv.rjust(7)}  {percent.rjust(4)}%\n"
    return s


def output_top_assets(l):
    # pp.pprint(l)
    s = '\n'
    s += '===========================================================================================\n'
    s += 'TOP        | Page   | %     |\n'
    s += 'STORIES    | Views  | of PV | \n'
    s += '-------------------------------------------------------------------------------------------\n'
    # remove items that don't have an asset number
    new_list = [item for item in l if (item['asset'] != 'unspecified')][:5]
    pp.pprint(new_list)
    for i, item in enumerate(new_list):
        # item['asset'] = item['asset'].replace('thespec|article|', '').replace('|none', '')
        info = get_online_asset_data(item['asset'])
        percent = str(item['%'])
        pv = "{:,}".format(item['pv'])
        percent = str(item['%'])
        asset = str(item['asset'])
        s += f"{i+1}. {asset.ljust(7)} {pv.rjust(8)}  {percent.rjust(4)}%    Author: {info['author']} | Section: {info['section']}\n"
        s += f"  Hed: {info['headline']}\n"
        s += "---------------------------------------------------------------------------------------\n"
    return s


def get_online_asset_data(i):
    time.sleep(2)

    url = f'https://www.guelphmercury.com/news-story/{str(i)}-abc/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    d_temp_data = {}

    # d_temp_data['author'] = soup.find('meta', name="author").get('content')
    # d_temp_data['author'] = author["content"]
    d_temp_data['headline'] = soup.find('h1', class_="ar-title").text
    # if soup.find('h2', class_="ar-sub-title"):
    # d_temp_data['deck'] = soup.find('h2', class_="ar-sub-titlear-title").text
    temp_site = soup.find("link", rel="canonical").get('href')
    d_temp_data['site'] = re.sub(r'https:\/\/www\.(.*)\.c(a|om)\/.*$', "\\1", temp_site)
    pp.pprint(d_temp_data['site'])
    # d_temp_data['section'] = soup.find("meta", property="article:section").get('content')
    if soup.find("script", type="application/ld+json"):
        # strict=False because sometimes we get people pasting in content from windows
        # leading to control characters \r in text
        raw_string = soup.find("script", type="application/ld+json").text
        raw_string = raw_string.replace('\n', ' ').replace('\r', '').replace('","publisher', '"],"publisher')
        print(raw_string)
        data_json = json.loads(raw_string, strict=False)

        d_temp_data['section'] = data_json['articleSection']
        d_temp_data['body'] = data_json['articleBody'].replace('\r\n', '')
        d_temp_data['deck'] = data_json['alternativeHeadline']

        # edge case two real authors in DNN article
        # "author":[{"@type":"Person","name":"Jon Wells","url":""},{"@type":"Person","name":"Natalie Paddon","url":""}],
        # one author
        # "author":{"@type":"Organization","name":"TheSpec.com","logo":{"@type":"ImageObject","url":"https://www.thespec.com/Contents/Images/Communities/TheSpec_600x60.png","width":600,"height":60}}

        d_temp_data['author'] = data_json['author']
        if isinstance(d_temp_data['author'], list):
            d_temp_data['author'] = data_json['author'][0]['name'] + data_json['author'][1]['name']
        else:
            d_temp_data['author'] = data_json['author']['name']
        if d_temp_data['author'] == "GuelphMercury.com":
            d_temp_data['author'] = d_temp_data['site']
    else:
        # d_temp_data['section'] = "NA"
        # d_temp_data['body'] = "NA"
        # d_temp_data['deck'] = "NA"
        d_temp_data['author'] = "CP Feed"
    # pp.pprint(d_temp_data)

    return {"headline": d_temp_data['headline'], "author": d_temp_data['author'], "section": d_temp_data['section']}

# [ MAIN ]--------------------------------


# DATA
# this dict will hold the final data in the form we want
# so we can easily retrieve it
data = {}
# holding string for output
output = ''

# READ PDF
text = process_pdf(config['pdf_name'])  # pdf -> a multi-line string

# PROCESS TEXT FROM PDF
staging_dict = parse_section(config, text)
pp.pprint(staging_dict)

# pp.pprint(parsed_text_dict)

data['summary'] = merge_lists(staging_dict['summary LW'], staging_dict['summary L90'], 'metric')
print(data['summary'])
# data['referrers'] = merge_lists(staging_dict['Referring domains yesterday'], staging_dict['Referring domains L90'], 'domain')
# data['device type'] = merge_lists(staging_dict['Device types yesterday'], staging_dict['Device types L90'], 'name')[:3]
# print("data device type")
# pp.pprint(data['device type'])
output += output_summary(data['summary'])
# output += output_referrers(data['referrers'])
# output += output_devices(data['device type'])
# output += output_top_assets(staging_dict['Spec top stories'])
# output += output_top_stories(staging_dict['Facebook top stories'], "FACEBOOK")
# output += output_top_stories(staging_dict['Twitter top stories'], "TWITTER")
# pp.pprint(data['summary'])

# print(staging_dict['Facebook top stories'])
# print("OUTPUT:")
print(output)
# pyperclip.copy(output)

# get date needs to be own function:
        # {
        #     "name": "report_date",
        #     "filter_lines": "year",
        #     "markers": {
        #         "start": "Sites summary yesterday",
        #         "end": "Report Suite"
        #     }

        # },
