from requests_html import HTMLSession
import re
import pprint
# import json

session = HTMLSession()

pp = pprint.PrettyPrinter(indent=2)


def get_online_asset_data(i):

    url = f'https://www.guelphmercury.com/news-story/{str(i)}-abc/'
    url = 'http://www.thestar.com/sports/bluejays/opinion/2018/03/08/guerrero-bichette-come-out-swinging-in-spring-debut-with-jays.html'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

    r = session.get(url)
    r.html.render()

    author_sel = '#app > div > div.sticky-replace-wrapper.clearfix > div:nth-child(2) > article > div.article__loader > div:nth-child(2) > div > div > div > div.show-right-rail > div > div.inset > div.article__byline > span.article__author > span:nth-child(1) > span > span:nth-child(1) > span > span > span > a > span'
    bob = r.html.find(author_sel, first=True)
    print(bob.text)
    # title = r.html.find('.ar-title', first=True)
    # print(title.text)
    # sel = 'head > link'
    # site_sel = r.html.find(sel, first=True).attrs['href']
    # site = re.sub(r'https:\/\/www\.(.*)\.c(a|om)\/.*$', "\\1", site_sel)
    # print(site)
    # tags_sel = '#tags'
    # r.html.render()
    # tags = r.html.find(tags_sel, first=True)
    # print(tags)
    # print(tags.find('a'))


get_online_asset_data(8317501)
