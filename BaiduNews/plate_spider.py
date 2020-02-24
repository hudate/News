# -*- coding:utf-8 -*-

import time
from threading import Thread

from lxml import etree, html

from BaiduNews.one_news import News
from common import get_data
from logger import Logger

logger = Logger('BDNews').logger


class PlateSpider(Thread):

    __parse1 = ['房产', '游戏']
    __parse2 = ['汽车', '互联网']
    __parse3 = ['首页', '科技', '财经', '国内', '女人', '体育', '军事', '国际', '娱乐']
    __dict = {
        '房产': 'house', '游戏': 'game', '汽车': 'auto', '互联网': 'internet', '首页': '', '科技': 'tech', '财经': 'finance',
        '国内': 'guonei', '女人': 'lady', '体育': 'sports', '军事': 'mil', '国际': 'guoji', '娱乐': 'ent',
    }

    def __init__(self, name, content):

        Thread.__init__(self, name=name)
        self.name = name
        self.content = content
        self.news = []
        self.author = []
        if name in self.__parse1:
            self.parse_data = self.parse_data1
        elif name in self.__parse2:
            self.parse_data = self.parse_data2
        elif name in self.__parse3:
            self.parse_data = self.parse_data3
        # self.parse_data = self.parse_data1 if self.name in self.__parse1 else self.parse_data2


    def parse_data1(self):
        tree = etree.HTML(self.content)
        uls = tree.xpath('//div[@class="tlc"]//ul')
        for ul in uls:
            ias = ul.xpath('li//a')
            for ia in ias:
                href = ia.xpath('@href')[0]
                title = ia.xpath('text()')[0]
                if 'baidu.com' in href:
                    self.news.append({
                        '标题': title,
                        '链接': href
                    })
        logger.info(self.name + '：' + str(self.news))
        return

    def parse_data2(self):
        if self.name == '互联网':
            url = 'http://news.baidu.com/widget?'
            params = {
                'id': 'AllOtherData',
                'channel': self.__dict[self.name],
                't': str(time.time() * 1000).split('.')[0]
            }
            self.content = get_data(url=url, params=params, plate=self.name)
            tree = etree.HTML(self.content)
            lis = tree.xpath('//div[contains(@class,"item")]')
        else:
            tree = etree.HTML(self.content)
            lis = tree.xpath('//li[@class="item"]')

        for li in lis:
            for ia in li.xpath('h3//a'):
                href = ia.xpath('@href')[0]
                title = ia.xpath('text()')[0]
                if 'baidu.com' in href:
                    self.news.append({
                        '标题': title,
                        '链接': href
                    })
        logger.info(self.name + '：' + str(self.news))
        return

    def parse_data3(self):
        tree = etree.HTML(self.content)
        uls = tree.xpath('//ul[contains(@class,"ulist")]')
        for ul in uls:
            ias = ul.xpath('li//a')
            for ia in ias:
                href = ia.xpath('@href')[0]
                title = ia.xpath('text()')[0]
                if 'baidu.com' in href:
                    self.news.append({
                        '标题': title,
                        '链接': href
                    })
        logger.info(self.name + '：' + str(self.news))
        return

    def get_author(self):
        for news in self.news:
            try:
                _news = News(news['链接'])
                _news.get_author()
                news['作者'] = _news.author
                self.author.append(_news.author)
            except Exception as e:
                logger.error(e)
        return













