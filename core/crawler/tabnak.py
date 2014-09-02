import logging
import re

from core.crawler.common import Crawler, ImageSanitizer


crawler_logger = logging.getLogger('crawler')

__author__ = 'SOROOSH'

cat_ids = {'1': 'cultural',
           '2': 'political',
           '3': 'social',
           '4': 'economic',
           '5': 'international',
           '6': 'foreign-political',
           '19': 'sport'
}


class TabnakCrawler(Crawler, ImageSanitizer):
    agencies = ['tabnak', 'yjc', 'bartarinha', 'mashregh']

    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        cat = None
        try:
            body = soup.find_all('div', {'class': 'body'})[0]
            self.sanitize_all_images(body, news)
            try:
                news_path_links = soup.find_all('div', {'class', 'news_path'})[0].find_all('a')
                for n in news_path_links:
                    m = re.search(r".*cat_id=(.*).*", n['href'], re.M | re.I)

                    if m:
                        try:
                            cat = cat_ids[m.group(1)]
                        except Exception as e:
                            cat = None
            except Exception as e:
                crawler_logger.error("Error occured in TabnakCrawler %s" % e)
                pass
        except Exception as e:
            body = "no content"

        return str(body), cat


# exp = r"cat_id=(.*?)"
# import re
#
# # m = re.search(r".*cat_id=(.*).*", 'http://gogle.com?cat_id=33', re.M | re.I)
# # print m.group()
# # print m.group(1)
# #
# c = TabnakCrawler()
#
#
# class A: pass
#
#
# a = A()
# a.link = 'http://www.tabnak.ir/fa/news/423398'
# print c.crawl_content(a)
#
# b=(1,2,3)
# print b[2]
#
