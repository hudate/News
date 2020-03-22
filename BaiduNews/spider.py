# -*- coding:utf-8 -*-
import sys
import threading

import requests
from bs4 import BeautifulSoup
from logger import Logger
from threading import Thread

URL = 'http://news.baidu.com'

logger = Logger('BDNews').logger


class BDNews(Thread):

    def __init__(self, name):
        Thread.__init__(self, name=name)
        self.name = name
        self.menu_dict = None
        self.plate_dict = {}
        self.plate_data = {}

    def parse_menu(self):
        data = self.__get_data()
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

    def __get_data(self, url=URL, plate=None):
        logger.info(url)
        req = None
        try_times = 1
        err_flag = 0
        while 1:
            try:
                req = requests.get(url, timeout=10)
                break
            except Exception as e:
                logger.error(e)
                try_times += 1

            if try_times == 4:
                err_flag = 1

        if (not plate) and (not err_flag) and req:
            return req.text

        if (not err_flag) and req and plate:
            logger.info(req)
            self.plate_dict[plate] = req

        if err_flag:
            logger.error('this request failed, url: %s' % url)
            sys.exit(1)

    def __parse_plate_data(self, content):
        soup = BeautifulSoup(content.text, 'html.parser')
        soup.find('')

    def get_plate_data(self):
        pool = []
        for menu_name, url in self.menu_dict.items():
            pool.append(Thread(target=self.__get_data, args=(url, menu_name)))
        [p.start() for p in pool]
        [p.join() for p in pool]

        pool = []
        for menu_name, content in self.plate_dict.items():
            pool.append(Thread(target=self.__parse_plate_data, args=(content, )))
        [p.start() for p in pool]
        [p.join() for p in pool]

    def run(self):
        self.parse_menu()
        self.get_plate_data()


if __name__ == '__main__':
    news = BDNews('baidu_news')
    news.run()

