from time import sleep
from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.context import RequestContext
from django.views.generic import View
from django.shortcuts import render_to_response
from core.models import News, AgencyRSSLink
from core.rss.parser import Parser


class HomeView(View):
    def get(self, request):
        return render_to_response('home.html', {'news': News.objects.all()[0:10]},
                                  context_instance=RequestContext(request))


class DetailView(View):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        return render_to_response('detail.html', {'news': news},
                                  context_instance=RequestContext(request))


class SimpleSearchView(View):
    def get(self, request):
        query = request.GET.get('q', None)
        page_number = request.GET.get('page_number', 1)
        if query == None:
            result = []
        else:
            result = News.objects.filter(title__icontains=query)

        paginator = Paginator(result, 10)

        return render_to_response('simple_search_result.html', {'query':query,'result': paginator.page(page_number)},
                                  context_instance=RequestContext(request))


