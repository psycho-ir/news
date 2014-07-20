__author__ = 'soroosh'

from core.models import NewsAgency
from django import template

register = template.Library()

@register.assignment_tag
def agencies():
    categories = NewsAgency.objects.all()
    return categories.all()





