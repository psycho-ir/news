from core.crawler.common import Crawler

__author__ = 'SOROOSH'


class IsnaCrawler(Crawler):
    agencies = ['isna']

    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        try:
            body = soup.find_all('div', {'class': 'body'})[0]
        except Exception as e:
            body = "no content"
        return str(body),None



