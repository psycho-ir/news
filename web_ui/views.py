from django.core.paginator import Paginator
from django.template.context import RequestContext
from django.views.generic import View
from django.shortcuts import render_to_response

from core.models import News


class HomeView(View):
    def get(self, request):
        return render_to_response('home.html', {'news': News.objects.all()[0:10]},
                                  context_instance=RequestContext(request))


class LoginView(View):
    def get(self, request):
        return render_to_response('login.html', {},
                                  context_instance=RequestContext(request))


class DetailView(View):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        liked = False
        if request.user.is_authenticated():
            if news.like_set.filter(user__id=request.user.id):
                liked = True
        news.liked = liked
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
        if int(page_number) > paginator.num_pages:
            page_number = paginator.num_pages

        page_result = []
        for item in paginator.page(page_number):
            item.liked = item.like_set.filter(user__id=request.user.id).exists()
            page_result.append(item)

        return render_to_response('simple_search_result.html',
                                  {'query': query, 'paginator': paginator.page(page_number), 'result': page_result},
                                  context_instance=RequestContext(request))


