"""
WSGI config for news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings_core")
import logging

from core.models import News, AgencyRSSLink, NewsDetail
from core.rss.parser import Parser
from price.service import update_prices
from scheduler.simple_scheduler import ThreadSimpleScheduler
from core.crawler import *


price_logger = logging.getLogger("price_scheduler")
rss_logger = logging.getLogger("rss_scheduler")
crawler_logger = logging.getLogger("crawler_scheduler")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def show_latest_news():
    all_links = AgencyRSSLink.objects.all()
    for link in all_links:
        latest_news = News.objects.filter(category__name=link.category_id, agency__name=link.agency_id).first()
        parser = Parser(link)
        if latest_news is not None:
            rss_logger.info('latest news added in: %s' % latest_news.date)
            new_news = parser.collect_news_after(date=latest_news.date)
        else:
            rss_logger.info('First news added')
            new_news = parser.collect_news_after()
        for n in new_news:
            rss_logger.info('News:%s is loaded' % n)
            n.save()


def crawl_some_news():
    selected_news = News.objects.filter(detail=None)[0:20]
    for n in selected_news:
        crawler_logger.info('News: %s with ID: %s loaded to crawl its content' % (n, n.id))
        detail_content, cat = get_crawler(n.agency_id).crawl_content(n)
        detail = NewsDetail()
        detail.news_id = n.id
        detail.content = detail_content
        detail.save()
        if cat:
            n.category_id = cat
            n.save()


scheduler = ThreadSimpleScheduler('RSS-READER', 180, show_latest_news)
# scheduler.run()

crawler_scheduler = ThreadSimpleScheduler('CRAWLER', 10, crawl_some_news)
# crawler_scheduler.run()

price_scheduler = ThreadSimpleScheduler('PRICE-READER', 1800, update_prices)
price_scheduler.run()