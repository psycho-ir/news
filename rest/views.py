from datetime import datetime
from django.core import serializers
from django.forms.models import model_to_dict
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
        result, serializer = self.get_api_result(request)
        p = Paginator(result, size)
        if int(page_number) > p.num_pages:
            return HttpResponse("{}")

        current_page = p.page(page_number)
        # response = serializers.serialize('json', current_page, indent=3)
        response = serializer(current_page)

        return HttpResponse(response)


class LatestNewsView(APIView):
    def get_api_result(self, request):
        import json

        def json_serial(obj):
            if isinstance(obj, datetime):
                serial = obj.isoformat()
                return serial

        def serializer(obj_list):
            result = []
            for obj in obj_list:
                dict = model_to_dict(obj)
                dict['likes'] = obj.like_set.count()
                dict['liked'] = obj.like_set.filter(user__id=request.user.id).exists()
                result.append(dict)

            return json.dumps(result, default=json_serial)


        agencies = request.GET.getlist('agencies', [])
        categories = request.GET.getlist('categories', [])
        all_news = News.objects.all()
        if len(agencies) > 0:
            all_news = all_news.filter(agency__in=agencies)

        if len(categories) > 0:
            all_news = all_news.filter(category__in=categories)

        return all_news, serializer


class LikeView(View):
    def post(self, request):
        news_id = request.POST.get('news_id', None)
        if not request.user.is_authenticated():
            return HttpResponse('{"message":"Not logined"}')
        if not Like.objects.filter(news__id=news_id, user__id=request.user.id).exists():
            like = Like()
            like.news_id = news_id
            like.user_id = request.user.id
            like.save()
            return HttpResponse('{"message":"Like saved"}')

        Like.objects.filter(news_id=news_id, user__id=request.user.id).delete()
        return HttpResponse('{"message":"Like removed"}')


class BookmarkView(View):
    def post(self, request):
        news_id = request.POST.get('news_id', None)
        if not request.user.is_authenticated():
            return HttpResponse('{"message":"Not logined"}')
        if not Bookmark.objects.filter(news__id=news_id, user__id=request.user.id).exists():
            bookmark = Bookmark()
            bookmark.news_id = news_id
            bookmark.user_id = request.user.id
            bookmark.save()
            return HttpResponse('{"message":"Bookmark saved"}')

        # Bookmark.objects.filter(news_id=news_id,user__id=request.user.id).delete()
        return HttpResponse('{"message":"Bookmark exist"}')



