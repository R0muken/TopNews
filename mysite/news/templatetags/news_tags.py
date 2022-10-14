from django import template
from django.db.models import Count

from news.models import Category, News


register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {'categories': categories}


@register.inclusion_tag('news/user_list_categories.html')
def show_user_categories(request):
    categories = Category.objects.filter(news__author=request.user.pk).distinct()
    return {'categories': categories}
