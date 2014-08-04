"""
WSGI config for news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from core.models import News, AgencyRSSLink, NewsDetail
from core.rss.parser import Parser
from price.service import update_prices
from scheduler.simple_scheduler import ThreadSimpleScheduler
from core.crawler import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def show_latest_news():
    all_links = AgencyRSSLink.objects.all()
    for link in all_links:
        latest_news = News.objects.filter(category__name=link.category_id, agency__name=link.agency_id).first()
        parser = Parser(link)
        if latest_news is not None:
            print 'latest news added in: %s' % latest_news.date
            new_news = parser.collect_news_after(date=latest_news.date)
        else:
            print 'First news added'
            new_news = parser.collect_news_after()
        for n in new_news:
            print 'News:%s is loaded' % n
            n.save()


def crawl_some_news():
    selected_news = News.objects.filter(detail=None)[:10]
    for n in selected_news:
        print 'News: %s with ID: %s loaded to crawl its content' % (n,n.id)
        detail_content = get_crawler(n.agency_id).crawl_content(n)
        detail = NewsDetail()
        detail.news_id = n.id
        detail.content = detail_content
        detail.save()


scheduler = ThreadSimpleScheduler(180, show_latest_news)
# scheduler.run()

crawler_scheduler = ThreadSimpleScheduler(10, crawl_some_news)
# crawler_scheduler.run()

price_scheduler = ThreadSimpleScheduler(1800,update_prices)
# price_scheduler.run()