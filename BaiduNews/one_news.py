# -*- coding:utf-8 -*-

from threading import Thread
import re

import bs4

from logger import Logger
from common import get_data
logger = Logger(__name__).logger


class News(Thread):

    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        self.content = None
        self.author = None

    def get_author(self):
        text = get_data(self.url)
        soup = bs4.BeautifulSoup(text, 'html.parser')
        try:
            author = soup.find('p', attrs={'class': 'author-name'})
            self.author = author.text
        except Exception as e:
            logger.error(e)

        if self.author == None:
            logger.error('出错url:' + self.url)

        return


if __name__ == '__main__':
    url = 'http://baijiahao.baidu.com/s?id=1659124402824041911'
    news = News(url)
    news.get_author()
