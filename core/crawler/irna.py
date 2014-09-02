from urllib2 import HTTPError

from core.crawler.common import Crawler


__author__ = 'SOROOSH'


class IrnaCrawler(Crawler):
    agencies = ['irna']

    def crawl_content(self, news):
        try:
            soup = self._get_soup(news.link)
        except HTTPError as http_error:
            if http_error.code == 404:
                return 'Deleted', None
        try:
            image = ''
            try:
                image = soup.find_all('img',
                                      {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent3_Image1'})[0]
            except Exception as e:
                pass

            body = soup.find_all('p', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent3_BodyLabel'})[0]
        except Exception as e:
            body = "no content"
        return str(image) + str(body), None





