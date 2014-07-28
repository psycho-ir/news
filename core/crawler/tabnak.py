from core.crawler.common import Crawler

__author__ = 'SOROOSH'


class TabnakCrawler(Crawler):
    agencies = ['tabnak']
    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        body = soup.find_all('div', {'class': 'body'})[0]
        return str(body)


crawler = TabnakCrawler()


class a:
    def __init__(self, link):
        self.link = link


result = crawler.crawl_content(a(
    'http://www.tabnak.ir/fa/news/419402'))
f = open('a.html', 'w')
f.write(result)

