from urllib2 import HTTPError

from core.crawler.common import Crawler


__author__ = 'SOROOSH'


class IsnaCrawler(Crawler):
    agencies = ['isna']

    def crawl_content(self, news):
        try:
            soup = self._get_soup(news.link)
        except HTTPError as http_error:
            if http_error.code == 404:
                return 'Deleted', None
        try:
            body = soup.find_all('div', {'class': 'body'})[0]
        except Exception as e:
            body = "no content"
        return str(body),None



