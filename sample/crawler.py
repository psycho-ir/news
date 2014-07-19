from abc import ABCMeta
import urllib2
from bs4 import BeautifulSoup


__author__ = 'soroosh'


class Crawler:
    __metaclass__ = ABCMeta




    class TabnakCrawler(Crawler):
        def __init__(self):
            self.base_url = 'https://tabnak.ir'

