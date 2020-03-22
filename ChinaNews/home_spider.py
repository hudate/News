# -*- coding:utf-8 -*-

import sys
import time
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup
from BaiduNews.plate_spider import PlateSpider
from logger import Logger
from threading import Thread

from settings import REAL, IS_ACCOUNT_AUTHOR

URL = 'http://news.baidu.com'

logger = Logger(__name__).logger


class BDNews(Process):

    def __init__(self, name, count_author_flag=False):
        Process.__init__(self)
        self.name = name
        self.menu_dict = None
        self.plate_dict = {}
        self.plate_data = {}
        self.news = {}
        self.author_count = {}
        self.author = {}
        self.count_author_flag = count_author_flag

    def parse_menu(self):
        while 1:
            data = self.__get_data()
            soup = BeautifulSoup(data, 'html.parser')
            menu = {}
            try:
                for li in soup.findAll('ul', attrs={'class': 'clearfix'})[1]:
                    a = li.find('a')
                    try:
                        menu[a.text] = URL + a['href']
                    except:
                        pass
            except:
                pass

            if menu:
                break

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
                req = requests.get(url, timeout=(10, 10))
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
            self.plate_dict[plate] = req.text

        if err_flag:
            logger.error('this request failed, url: %s' % url)
            sys.exit(1)

    def get_plate_data(self):
        pool = []
        for menu_name, url in self.menu_dict.items():
            pool.append(Thread(target=self.__get_data, args=(url, menu_name)))
        [p.start() for p in pool]
        [p.join() for p in pool]

        for menu_name, content in self.plate_dict.items():
            plate_spider = PlateSpider(menu_name, content)
            plate_spider.parse_data()
            if self.count_author_flag:
                plate_spider.get_author()

            if plate_spider.news == []:
                logger.warning(plate_spider.name)
                logger.error(plate_spider.news)

            self.news[menu_name] = plate_spider.news
            self.author[menu_name] = plate_spider.author

    def count_author(self):
        for k, v in self.author.items():
            author_count = {}
            for author in v:
                if author in author_count:
                    author_count[author] += 1
                else:
                    author_count[author] = 1
            self.author_count[k] = author_count

    def run(self):
        self.parse_menu()
        self.get_plate_data()
        self.count_author()


if __name__ == '__main__':

    i = 0
    t = []

    max_times = 1

    if REAL:
        max_times = 5

    news = None
    while i < max_times:
        t1 = time.time()
        news = BDNews(name='baidu_news', count_author_flag=IS_ACCOUNT_AUTHOR)
        news.run()
        delta_time = time.time() - t1
        t.append(delta_time)
        i += 1

    logger.info(news.news)

    if IS_ACCOUNT_AUTHOR:
        logger.info(news.author_count)

    for k, v in news.news.items():
        logger.info(k, len(v))

    if not REAL:
        logger.info(sum(t) / len(t))

