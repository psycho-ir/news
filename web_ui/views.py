from time import sleep
from django.shortcuts import render
from django.template.context import RequestContext
from django.views.generic import View
from django.shortcuts import render_to_response
from core.models import News, AgencyRSSLink
from core.rss.parser import Parser


class HomeView(View):
    def get(self, request):
        # rss_links = AgencyRSSLink.objects.all()
        # for link in rss_links:
        #     parser = Parser(link)
        #     news_list = parser.collect_news_after()
        #
        #     for n in news_list:
        #         n.save()
        #
        #

        return render_to_response('home.html', {'news': News.objects.all()[0:10]},
                                  context_instance=RequestContext(request))


class DetailView(View):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        return render_to_response('detail.html', {'news': news},
                                  context_instance=RequestContext(request))
