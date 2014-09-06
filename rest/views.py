# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal
import json

from jdatetime import datetime as jalali_datetime
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.generic import View
from django.core.paginator import *

from core.models import News, Like, Bookmark, NewsCategory
from price.models import Price, Item


def json_serial(obj):
    if isinstance(obj, datetime):
        serial = jalali_datetime.fromgregorian(datetime=obj)

        return "%s %s %s در ساعت %s:%s:%s" % (serial.day, jalali_datetime.j_months_fa[serial.month - 1], serial.year, serial.hour, serial.minute, serial.second)

    elif isinstance(obj, date):
        serial = str(jalali_datetime.fromgregorian(date=obj))
        return serial

    if isinstance(obj, Decimal):
        return str(obj)


class APIView(View):
    def get_api_result(self, request):
        pass

    def get(self, request):
        page_number = request.GET.get('page_number', 1)
        size = request.GET.get('size', 10)
        result, serializer = self.get_api_result(request)
        p = Paginator(result, size)
        if int(page_number) > p.num_pages:
            return HttpResponse("[]")

        current_page = p.page(page_number)
        # response = serializers.serialize('json', current_page, indent=3)
        response = serializer(current_page)

        return HttpResponse(response)


class LatestNewsView(APIView):
    def get_api_result(self, request):

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


class ListBookmarkView(APIView):
    def get_api_result(self, request):
        def serializer(obj_list):
            result = []
            for obj in obj_list:
                dict = model_to_dict(obj.news)
                dict['likes'] = obj.news.like_set.count()
                dict['liked'] = obj.news.like_set.filter(user__id=request.user.id).exists()
                result.append(dict)

            return json.dumps(result, default=json_serial)

        if request.user.is_authenticated():
            bookmarks = Bookmark.objects.filter(user__id=request.user.id).order_by('-id')
            return bookmarks, serializer
        else:
            return [], serializer


class AllCategories(View):
    def get(self, request):
        categories = NewsCategory.objects.all().exclude(name='important')
        return HttpResponse(serializers.serialize('json', categories), mimetype='application/json')


class PriceView(View):
    def get(self, request):
        result = []
        for item in Item.objects.all():

            item__first = Price.objects.filter(item=item).first()
            if item__first is not None:
                result.append(model_to_dict(item__first))

        return HttpResponse(json.dumps(result, default=json_serial))


class DateView(View):
    def get(self, request):
        last_update_date = jalali_datetime.fromgregorian(datetime=News.objects.first().date)
        today = jalali_datetime.now()
        if last_update_date > today:
            last_update_date = today
        result = {'latest': '%s %s %s در ساعت %s:%s:%s' % (
            last_update_date.day, jalali_datetime.j_months_fa[last_update_date.month - 1], last_update_date.year, last_update_date.hour, last_update_date.minute, last_update_date.second),
                  'today': "%s %s %s" % (today.day, jalali_datetime.j_months_fa[today.month - 1], today.year )}
        return HttpResponse(json.dumps(result))


