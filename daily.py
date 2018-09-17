import defaults
import utils_text
import utils_nums
import templates
import string
import sys
import requests
from bs4 import BeautifulSoup
import re
import pprint
import time
import json
import pyperclip
import smartypants

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


def parse_section(config, ms):
    # takes multiline string and extracts chunk based on markers in config's sections
    # then cleans the section of unwanted spaces
    # then turns into list of strings (lines)
    staging = {"site": config['site'], "report": config['report']}
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
        clean_lines = utils_text.lines(utils_text.find_between(ms, item['markers']['start'], item['markers']['end']))
        # print(clean_lines)
        # print("+++++++++")

        # trims x number of lines from top and bottom
        # this assumes the data we want is a contiguous run of lines in the middle
        if item['trim']:
            clean_lines = clean_lines[item['trim'][0]:item['trim'][1]]

        # Tweak each line to remove or replace as noted in config:
        # each line comes back a list of strings
        # print("Matched lines:")
        # pp.pprint(matched_lines)
        # print("")

        modified_lines = [utils_text.line_modify(line, item['remove'], item['subs']) for line in clean_lines]
        # print("Modified lines:")
        # pp.pprint(modified_lines)
        # print("")
        # Turn each line into dict with keys based on config['keys']
        objectified_lines = [utils_text.line_objectify(line, item['keys']) for line in modified_lines]

        # Add all this text to the holding list 'staging'
        # grouped under the section name
        new_dict_key = item['name']
        new_dict_value = objectified_lines
        # new_dict = {new_dict_key: new_dict_value}
        # staging.append(new_dict)
        staging[new_dict_key] = new_dict_value
    return staging

# [ UTLITY FUNCTIONS ]--------------


def get_online_asset_data(i, info="all"):
    print(f"Fetching details on asset #{str(i)}")
    time.sleep(4)

    url = f'https://www.guelphmercury.com/news-story/{str(i)}-abc/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    d_temp_data = {}

    # d_temp_data['author'] = soup.find('meta', name="author").get('content')
    # d_temp_data['author'] = author["content"]
    if soup.find('h1', class_="ar-title"):
        d_temp_data['headline'] = soup.find('h1', class_="ar-title").text
        # if soup.find('h2', class_="ar-sub-title"):
        # d_temp_data['deck'] = soup.find('h2', class_="ar-sub-titlear-title").text
        temp_site = soup.find("link", rel="canonical").get('href')
        d_temp_data['site'] = re.sub(r'https:\/\/www\.(.*)\.c(a|om)\/.*$', "\\1", temp_site)
        # pp.pprint(d_temp_data['site'])
        # d_temp_data['section'] = soup.find("meta", property="article:section").get('content')
        if soup.find("script", type="application/ld+json"):
            # strict=False because sometimes we get people pasting in content from windows
            # leading to control characters \r in text
            raw_string = soup.find("script", type="application/ld+json").text
            raw_string = raw_string.replace('\n', ' ').replace('\r', '').replace('","publisher', '"],"publisher')
            # raw_string = smartypants.smartypants(raw_string)
            # TROUBLESHOOTING
            # print(raw_string)
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
            d_temp_data['section'] = "NA"
            d_temp_data['body'] = "NA"
            d_temp_data['deck'] = "NA"
            d_temp_data['author'] = "CP Feed"
        # pp.pprint(d_temp_data)

        if info == "headline":
            return d_temp_data['headline']
        else:
            return {"headline": d_temp_data['headline'], "author": d_temp_data['author'], "section": d_temp_data['section']}
    else:
        return {"headline": str(i), "author": "NA", "section": "NA"}


def check_input(arguments):
    if len(arguments) == 3:
        report = f'{sys.argv[1]}'
        site = f'{sys.argv[2]}'
        return (f'{sys.argv[1]}', f'{sys.argv[2]}')
    else:
        print("Choices: daily spectator | daily record | weekly spectator")
        return None

# [ DATA MUNGING ]--------------------------------


def top_fb_stories(l, limit):
    total_pv = utils_text.find_dict_in_list(staging_dict['referring domains ys'], 'domain', 'facebook.com')['pv']
    temp_list = utils_text.reduce_list_of_dicts(l, 'asset', 'pv')[:limit]
    # add % of total PVs of from social network
    for item in temp_list:
        item['%'] = utils_nums.percent(item['pv'], total_pv)
        item['headline'] = get_online_asset_data(item['asset'], "headline")
    return temp_list


def top_tco_stories(l, limit):
    total_pv = utils_text.find_dict_in_list(staging_dict['referring domains ys'], 'domain', 't.co')['pv']
    temp_list = utils_text.reduce_list_of_dicts(l, 'asset', 'pv')[:limit]
    # add % of total PVs of from social network
    for item in temp_list:
        item['%'] = utils_nums.percent(item['pv'], total_pv)
        if isinstance(item['asset'], int):
            item['headline'] = get_online_asset_data(item['asset'], "headline")
        else:
            item['headline'] = string.capwords(item['asset'].replace('http://3downnation.com/2018/', '3Down:').replace('-', ' '))

    return temp_list


def top_stories(l, limit):
    temp_list = [item for item in l if (item['asset'] != 'unspecified')][:limit]
    for item in temp_list:
        item['article_info'] = get_online_asset_data(item['asset'])
        item['article_info']['section'] = ','.join(list(set(item['article_info']['section'].replace('|', ' ').replace(',', ' ').split(" "))))
    return temp_list


def report_date(l):
    temp = l[0]
    return f"{temp['day']} {temp['month']} {temp['date']} {temp['year']}"


def device_types(l_new, l_old, key):
    temp_list = utils_text.merge_lists(l_new, l_old, key)
    # now parse temp list, peforming calculations
    for item in temp_list:
        item['name'] = item['name'].replace('-', ' ').replace('Other', 'Desktop').replace(' Phone', '')
        item['diff_pv%'] = utils_nums.diff(item['pv'], item['pv_l90'], '%90')
        item['diff_ratio'] = round((item['%'] - item['%_l90']), 1)
    return temp_list


def referrers(l_new, l_old, key, site):
    temp_list = utils_text.merge_lists(l_new, l_old, key)
    # cleanup  list, convert all google domains to just 'google'
    for item in temp_list:
        item['domain'] = item['domain'].replace('/Bookmarked', '').replace('.com', '').replace('t.co', 'twitter').replace('m.', '')
        if 'google' in item['domain']:
            item['domain'] = 'google'

    temp_list_2 = utils_text.reduce_list_of_dicts(temp_list, 'domain', ['pv', 'pv_l90'])
    total_pv = utils_text.find_dict_in_list(staging_dict['summary ys'], 'name', site)['pv']
    # now parse temp list, peforming calculations
    for item in temp_list_2:
        item['diff_pv%'] = utils_nums.diff(item['pv'], item['pv_l90'], '%90')
        item['pv_ratio'] = utils_nums.percent(item['pv'], total_pv)
        item['pv_ratio'] = round(((item['pv'] / total_pv) * 100), 1)
    return temp_list_2


def summary(l_new, l_old, key, site):
    temp_list = utils_text.merge_lists(l_new, l_old, key)
    print("New merged list")
    site_stats = [item for item in temp_list if item["name"] == site][0]
    metro_stats = [item for item in temp_list if item["name"] == "Metroland"][0]
    new_stat = {"name": "R of M"}
    keys = ['pv', 'pv_l90', 'uv', 'uv_l90', 'v', 'v_l90']
    for item in keys:
        new_stat[item] = (metro_stats[item] - site_stats[item])
    temp_list.append(new_stat)
    for item in temp_list:
        item['pv vs ma'] = utils_nums.diff(item['pv'], item['pv_l90'], '%90')
        item['pv / uv'] = round((item['pv'] / item['uv']), 2)
        item['visits vs ma'] = utils_nums.diff(item['v'], item['v_l90'], '%90')
        item['pv / v'] = round((item['pv'] / item['v']), 2)
    new_list = sorted(temp_list, key=lambda k: k['pv'], reverse=True)
    return new_list

# [ MAIN ]--------------------------------


report = check_input(sys.argv)
if report:
    # DATA
    # this dict will hold the final data in the form we want
    # so we can easily retrieve it
    data = {}
    # holding string for output
    output = ''

    report_type = report[0]
    site = report[1]
    this_default = defaults.config['report'][report_type][site]

    # READ PDF, extract text
    text = utils_text.process_pdf(this_default['pdf_name'])  # pdf -> a multi-line string
    # print("================\nRaw text from PDF:\n================")
    # print(text)

    # PROCESS TEXT FROM PDF
    staging_dict = parse_section(this_default, text)
    with open('working/staging.json', 'w') as outfile:
        json.dump(staging_dict, outfile)
    # print('================\nStaging dict:\n================')
    # pp.pprint(staging_dict)

    # MUNGE DATA INTO FINAL 'DATA' DICTIONARY FOR FINAL OUTPUT
    data['site'] = defaults.config['report'][report_type][site]['site']
    data['report date'] = report_date(staging_dict['report date'])
    data['top stories'] = top_stories(staging_dict['top stories'], this_default['fetch_limits']['top stories'])
    data['referrers'] = referrers(staging_dict['referring domains ys'], staging_dict['referring domains l90'], 'domain', data['site'])[:5]
    data['device types'] = device_types(staging_dict['device types ys'], staging_dict['device types l90'], 'name')[:3]
    data['facebook top stories'] = top_fb_stories(staging_dict['facebook top stories'], this_default['fetch_limits']['Facebook'])
    data['twitter top stories'] = top_tco_stories(staging_dict['twitter top stories'], this_default['fetch_limits']['Twitter'])
    data['summary'] = summary(staging_dict['summary ys'], staging_dict['summary l90'], 'name', data['site'])
    with open('working/data.json', 'w') as outfile:
        json.dump(data, outfile)
    # pp.pprint(data)
    output = templates.template_daily(data)
    print(output)

    # print(output)
    pyperclip.copy(output)
