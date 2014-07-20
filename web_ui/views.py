from time import sleep
from django.shortcuts import render
from django.template.context import RequestContext
from django.views.generic import View
from django.shortcuts import render_to_response
from core.models import News
from sample.rss_reader.parser import Parser


class HomeView(View):
    def get(self, request):
        # parser = Parser('http://www.tabnak.ir/fa/rss/allnews')
        # news_list = parser.collect_news_after()
        #
        # for n in news_list:
        # n.save()
        #
        # while True:
        # sleep(1)
        #
        # new_feeds = parser.collect_news_after(date=None)
        # if new_feeds is None:
        #         print 0
        #     else:
        #         print(len(new_feeds))

        return render_to_response('home.html', {'news': News.objects.all()[:10]},
                                  context_instance=RequestContext(request))


class DetailView(View):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        return render_to_response('detail.html', {'news': news},
                                  context_instance=RequestContext(request))
