from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    local_name = models.CharField(max_length=500)


class Price(models.Model):
    item = models.ForeignKey(Item)
    date = models.DateField()
    price = models.IntegerField()



