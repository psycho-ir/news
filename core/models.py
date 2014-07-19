from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.CharField(max_length=500)
    link = models.CharField(max_length=300)
    date = models.DateTimeField()

