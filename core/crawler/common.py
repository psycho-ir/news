import urllib2
from bs4 import BeautifulSoup

__author__ = 'soroosh'

crawler_registry = {}


class CrawlerMeta(type):
    def __init__(cls, what, bases=None, dict=None):
        super(CrawlerMeta, cls).__init__(what, bases, dict)
        print('Crawler:%s is loading' % what)
        if hasattr(cls, 'agencies'):
            crawler = cls()
            for agency in cls.agencies:
                crawler_registry[agency] = crawler


class Crawler:
    __metaclass__ = CrawlerMeta

    def crawl_content(self, news): raise NotImplementedError()

    def _get_soup(self, link):
        response = urllib2.urlopen(link)
        html = response.read()
        soup = BeautifulSoup(html)

        return soup

