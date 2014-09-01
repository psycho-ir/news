import urllib
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
        response = urllib2.urlopen(urllib.quote(link.replace('\n', '').encode('utf-8'), safe=':/'))
        html = response.read()
        soup = BeautifulSoup(html)

        return soup


class ImageSanitizer:
    def sanitize_all_images(self, body, news):
        all_imgs = body.find_all('img')
        for img in all_imgs:
            if img.attrs['src'] is not None and img.attrs['src'].strip()[0] == '/':
                img.attrs['src'] = news.agency.url + img.attrs['src']



