# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from jdatetime import datetime as jalali_datetime


class NewsAgency(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    local_name = models.CharField(max_length=200)
    img_address = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    local_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class AgencyRSSLink(models.Model):
    link = models.CharField(max_length=250)
    category = models.ForeignKey(NewsCategory)
    agency = models.ForeignKey(NewsAgency, related_name='rss_links')


class News(models.Model):
    class Meta:
        ordering = ['-date']

    title = models.CharField(max_length=200)
    abstract = models.CharField(max_length=500)
    link = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField()
    category = models.ForeignKey(NewsCategory)
    agency = models.ForeignKey(NewsAgency)
    important = models.BooleanField(default=False)

    def get_persian_date(self):
        serial = jalali_datetime.fromgregorian(datetime=self.date)
        return "%s %s %s در ساعت %s:%s:%s" % (serial.day, jalali_datetime.j_months_fa[serial.month - 1], serial.year, serial.hour, serial.minute, serial.second)

    def __unicode__(self):
        return self.title


class NewsDetail(models.Model):
    news = models.OneToOneField(News, primary_key=True, related_name='detail')
    content = models.TextField()

    def __unicode__(self):
        return self.news.title


class Like(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)


class Bookmark(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)





