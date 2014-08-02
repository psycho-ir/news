from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    local_name = models.CharField(max_length=500)


class Price(models.Model):
    class Meta:
        ordering = ['-date']
    item = models.ForeignKey(Item)
    date = models.DateField()
    price = models.DecimalField(decimal_places=2,max_digits=14)



