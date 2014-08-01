from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.core.paginator import *
from core.models import News, Like, Bookmark


class APIView(View):
    def get_api_result(self, request): pass

    def get(self, request):
        page_number = request.GET.get('page_number', 1)
        size = request.GET.get('size', 10)
        result = self.get_api_result(request)
        p = Paginator(result, size)
        if int(page_number) > p.num_pages:
            page_number = p.num_pages

        current_page = p.page(page_number)
        response = serializers.serialize('json', current_page, indent=3)

        return HttpResponse(response)


class LatestNewsView(APIView):
    def get_api_result(self, request):
        agencies = request.GET.getlist('agencies', [])
        categories = request.GET.getlist('categories', [])
        all_news = News.objects.all()
        if len(agencies) > 0:
            all_news = all_news.filter(agency__in=agencies)

        if len(categories) > 0:
            all_news = all_news.filter(category__in=categories)

        return all_news


class LikeView(View):
    def post(self, request):
        news_id = request.POST.get('news_id', None)
        if not Like.objects.filter(news__id=news_id, user__id=request.user.id):
            like = Like()
            like.news_id = news_id
            like.user_id = request.user.id
            like.save()
            return HttpResponse("Like saved")

        return HttpResponse("Like exist")


class BookmarkView(View):
    def post(self, request):
        news_id = request.POST.get('news_id', None)
        if not Bookmark.objects.filter(news__id=news_id, user__id=request.user.id):
            bookmark = Bookmark()
            bookmark.news_id = news_id
            bookmark.user_id = request.user.id
            bookmark.save()
            return HttpResponse("Bookmark saved")

        return HttpResponse("Bookmark exist")



