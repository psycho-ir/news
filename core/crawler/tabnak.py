from core.crawler.common import Crawler

__author__ = 'SOROOSH'


class TabnakCrawler(Crawler):
    agencies = ['tabnak','yjc']

    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        try:
            body = soup.find_all('div', {'class': 'body'})[0]
        except Exception as e:
            body = "no content"
        return str(body)



