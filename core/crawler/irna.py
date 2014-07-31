from core.crawler.common import Crawler

__author__ = 'SOROOSH'


class IrnaCrawler(Crawler):
    agencies = ['irna']

    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        try:
            body = soup.find_all('div', {'class': 'BodyText'})[0]
        except Exception as e:
            body = "no content"
        return str(body)





