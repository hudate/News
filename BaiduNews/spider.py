# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

URL = 'http://news.baidu.com'


class BDNews(object):

    def __init__(self, name):
        self.name = name
        self.menu_dict = None

    def parse_menu(self):
        data = self.get_data()
        soup = BeautifulSoup(data, 'html.parser')
        menu = {}
        for li in soup.findAll('ul', attrs={'class': 'clearfix'})[1]:
            a = li.find('a')
            try:
                menu[a.text] = URL + a['href']
            except Exception as e:
                print(e, li)
        if menu:
            self.menu_dict = menu
        return menu

    def get_data(self, url=URL):
        req = requests.get(url, timeout=10)
        return req.text


if __name__ == '__main__':
    news = BDNews('baidu_news')
    news.parse_menu()
    print(news.menu_dict)

