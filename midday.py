import pdftotext
import requests
from bs4 import BeautifulSoup
import re
import pprint
import time
import json
import pyperclip


pp = pprint.PrettyPrinter(indent=2)

# GENERATE MIDDAY REPORT

config = {
    "pdf_name": "pdfs_new/Daily midday.pdf",
    "sections": [
        {
            "markers":
            {
                "start": "Spec Top AssetID today",
                "end": "Rec Top AssetID today"
            },
            "site": "Spectator",
            "filter_lines": "percent",
            "remove": [',', '%'],
            "targets": [],
            "subs": [],
            "keys": [
                # tuples where [0] is field name, [1] is field position
                ('rank', 0),
                ('asset', 1),
                ('pv', 2),
                ('%', 3),
            ],
            "limit": 5,
        },
        {
            "markers":
            {
                "start": "Rec Top AssetID today",
                "end": "GMT Top AssetIDs midday"
            },
            "site": "Record",
            "filter_lines": "percent",
            "targets": [],
            "subs": [],
            "remove": [',', '%'],
            "keys": [
                # tuples where [0] is field name, [1] is field position
                ('rank', 0),
                ('asset', 1),
                ('pv', 2),
                ('%', 3),
            ],
            "limit": 4,
        },
        {
            "markers":
            {
                "start": "GMT Top AssetIDs midday",
                "end": "Page 2 of 2"
            },
            "site": "Guelph MercTrib",
            "filter_lines": "percent",
            "targets": [],
            "subs": [],
            "remove": [',', '%'],
            "keys": [
                # tuples where [0] is field name, [1] is field position
                ('rank', 0),
                ('asset', 1),
                ('pv', 2),
                ('%', 3),
            ],
            "limit": 3,
        },
    ]
}


def parse_section(config, ms):
    staging = {}
    for item in config['sections']:
        clean_lines = lines(find_between(ms, item['markers']['start'], item['markers']['end']))
        if item['filter_lines'] == 'number-comma':
            matched_lines = [line for line in clean_lines if bool(re.search(r'\d,\d', line))]
            if 'Total' in matched_lines[-1]:
                matched_lines = matched_lines[:-1]
        if item['filter_lines'] == 'percent':
            matched_lines = [line for line in clean_lines if '%' in line]
        modified_lines = [line_modify(line, item['remove'], item['targets'], item['subs']) for line in matched_lines]
        objectified_lines = [line_objectify(line, item['keys']) for line in modified_lines]
        new_dict_key = item['site']
        new_dict_value = objectified_lines
        staging[new_dict_key] = new_dict_value

    return staging


def output_top_assets(d):
    # a dict of
    # staging dict { "spec" : [], "rec": [], "gmt": [] }
    # pp.pprint(l)
    s = ''
    for k, v in d.items():
        s += '\n'
        s += '===========================================================================================\n'
        s += f'{k.ljust(12)}| Page   | %     |\n'
        s += 'TOP STORIES | Views  | of PV | \n'
        s += '-------------------------------------------------------------------------------------------\n'
        # remove items that don't have an asset number

        new_list = [item for item in v if (item['asset'] != 'unspecified')][:4]
        for i, item in enumerate(new_list):
            # item['asset'] = item['asset'].replace('thespec|article|', '').replace('|none', '')
            info = get_online_asset_data(item['asset'])
            percent = str(item['%'])
            pv = "{:,}".format(item['pv'])
            percent = str(item['%'])
            asset = str(item['asset'])
            s += f"{i+1}. {asset.ljust(7)} {pv.rjust(8)}   {percent.rjust(5)}%   Author: {info['author']} | Section: {info['section']}\n"
            s += f"   Hed: {info['headline']}\n"
            s += "---------------------------------------------------------------------------------------\n"
    return s


# [ UTLITY FUNCTIONS ]--------------


def process_pdf(f):
    memory_file = open(f, 'rb')
    pdf = pdftotext.PDF(memory_file)
    memory_file.close()
    pdf_text = ""
    for page in pdf:
        pdf_text += page
    return pdf_text


def find_between(ms, first, last):
    try:
        start = ms.index(first) + len(first)
        end = ms.index(last, start)
        return ms[start:end]
    except ValueError:
        return ""


def lines(ms):
    return [" ".join(line.strip().split()) for line in ms.splitlines() if line != '']


def file_name(s):
    pass


text = lines(process_pdf('pdfs_new/Daily midday.pdf'))[4]  # pdf -> a multi-line string
text = '_'.join(text.replace('.', '').split()[1:4])


def line_modify(s, list_remove, list_targets, list_replacements):
    for item in list_remove:
        s = s.replace(item, '')
    for index, item in enumerate(list_targets):
        s = s.replace(item, list_replacements[index])
    new_line = re.sub(r"^(\d{1,2})\. ", "\\1 ", s)
    new_line = re.sub(r"([a-zA-Z]) (\(?[a-zA-Z])", "\\1-\\2", new_line)
    new_list = new_line.split()
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
    return {k[0]: l_line[k[1]] for k in t_keys}


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
    # d_temp_data['section'] = soup.find("meta", property="article:section").get('content')
    if soup.find("script", type="application/ld+json"):
        # strict=False because sometimes we get people pasting in content from windows
        # leading to control characters \r in text
        data_json = json.loads(soup.find("script", type="application/ld+json").text, strict=False)
        d_temp_data['section'] = data_json['articleSection']
        # d_temp_data['body'] = data_json['articleBody'].replace('\r\n', '')
        # d_temp_data['deck'] = data_json['alternativeHeadline']
        d_temp_data['author'] = data_json['author']['name']
        if d_temp_data['author'] == "GuelphMercury.com":
            d_temp_data['author'] = d_temp_data['site']
    else:
        d_temp_data['section'] = "NA"
        # d_temp_data['body'] = "NA"
        # d_temp_data['deck'] = "NA"
        d_temp_data['author'] = "CP Feed"
    print("Processing ...")
    # pp.pprint(d_temp_data)

    return {"headline": d_temp_data['headline'], "author": d_temp_data['author'], "section": d_temp_data['section']}

# [ MAIN ]--------------------------------


data = {}
output = ''

text = process_pdf(config['pdf_name'])  # pdf -> a multi-line string
# print(text)

# PROCESS TEXT FROM PDF
staging_dict = parse_section(config, text)

# pp.pprint(staging_dict)

output += output_top_assets(staging_dict)
print(output)
pyperclip.copy(output)

query = input("OK to archive PDF? (y/n)")
if query == 'y':
    pass
