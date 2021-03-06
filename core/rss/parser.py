import datetime
from time import sleep

from core.models import News


__author__ = 'soroosh'

import feedparser


class Parser:
    def __init__(self, agencyRSSLink):
        self.agencyRSSLink = agencyRSSLink

    def collect_news_after(self, **kwargs):
        if kwargs.get('date') == None:
            def is_selectable(d):
                return True

        else:
            def is_selectable(d):
                if d < kwargs.get('date'):
                    return False
                return True
        print 'reading rss feeds from:%s category:%s agency:%s' % (
            self.agencyRSSLink.link, self.agencyRSSLink.category_id, self.agencyRSSLink.agency_id)
        parsed = feedparser.parse(self.agencyRSSLink.link)
        print 'parsing completed...'
        result = list()
        for item in parsed['items']:
            try:
                d = datetime.datetime.strptime(item.published[0:20], '%d %b %Y %H:%M:%S')
            except:
                d = datetime.datetime.strptime(item.published[5:25], '%d %b %Y %H:%M:%S') + datetime.timedelta(
                    minutes=30, hours=4)
            if not is_selectable(d):
                continue
            news = News()
            news.agency_id = self.agencyRSSLink.agency.name
            news.category_id = self.agencyRSSLink.category.name
            if self.agencyRSSLink.category.name == 'important':
                news.important = True
            news.title = item.title
            if hasattr(item, 'description'):
                news.abstract = item.description
            news.link = item.link
            news.date = d
            # item.title, '', item.link, d
            result.append(news)

        return result


if __name__ == '__main__':
    parser = Parser('http://www.tabnak.ir/fa/rss/allnews')
    news_list = parser.collect_news_after()
    print(len(news_list))
    print(news_list[0].date)

    while True:
        sleep(1)

        new_feeds = parser.collect_news_after(date=None)
        if new_feeds is None:
            print 0
        else:
            print(len(new_feeds))




