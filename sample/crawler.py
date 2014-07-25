from abc import ABCMeta
import urllib2
from bs4 import BeautifulSoup


__author__ = 'soroosh'


class Crawler:
    __metaclass__ = ABCMeta

    def crawl_content(self, news): raise NotImplementedError()

    def _get_soup(self, link):
        response = urllib2.urlopen(link)
        html = response.read()
        soup = BeautifulSoup(html)

        return soup


class TabnakCrawler(Crawler):
    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        body = soup.find_all('div', {'class': 'body'})
        print str(body)
        print 'hehe'


# #main

crawler = TabnakCrawler()


class a:
    def __init__(self, link):
        self.link = link


crawler.crawl_content(a('http://www.tabnak.ir/fa/news/419436/%DA%AF%D8%B1%D8%A7%D9%86%D8%AA%D8%B1%D9%8A%D9%86-%D8%AE%D8%B7-%D8%AD%D9%85%D9%84%D9%87-%D8%AA%D8%A7%D8%B1%D9%8A%D8%AE-%D8%AF%D8%B1-%D8%B1%D8%A6%D8%A7%D9%84-%D9%85%D8%A7%D8%AF%D8%B1%D9%8A%D8%AF'))
