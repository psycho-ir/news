import re

from core.crawler.common import Crawler


__author__ = 'SOROOSH'

cat_ids = {'1': 'cultural',
           '2': 'political',
           '3': 'social',
           '4': 'economic',
           '5': 'international',
           '6': 'foreign-political',
           '19': 'sport'
}


class TabnakCrawler(Crawler):
    agencies = ['tabnak', 'yjc', 'bartarinha', 'mashregh']

    def crawl_content(self, news):
        soup = self._get_soup(news.link)
        cat = None
        try:
            body = soup.find_all('div', {'class': 'body'})[0]
            print body
            print 0
            try:
                print 1
                news_path_links = soup.find_all('div', {'class', 'news_path'})[0].find_all('a')
                print 2
                for n in news_path_links:
                    print 3
                    m = re.search(r".*cat_id=(.*).*", n['href'], re.M | re.I)

                    if m:
                        print 4
                        try:
                            cat = cat_ids[m.group(1)]
                        except Exception as e:
                            cat = None
            except Exception as e:
                pass
        except Exception as e:
            body = "no content"

        print 'returning'
        print cat
        print type(body)
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
