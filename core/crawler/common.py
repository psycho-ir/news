import urllib
import urllib2
from bs4 import BeautifulSoup
import re

__author__ = 'soroosh'

crawler_registry = {}
strip_unicode = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")


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
        response = urllib2.urlopen(urllib.quote(strip_unicode.sub('',link).replace('\n', ''), safe=':/'))
        html = response.read()
        soup = BeautifulSoup(html)

        return soup

