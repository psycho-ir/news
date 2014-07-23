from django.db import models


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
    link = models.CharField(max_length=300)
    date = models.DateTimeField()
    category = models.ForeignKey(NewsCategory)
    agency = models.ForeignKey(NewsAgency)
    content = models.TextField()

    def __unicode__(self):
        return self.title



