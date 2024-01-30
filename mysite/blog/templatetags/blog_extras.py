import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

register = template.Library()


@register.filter
def ru_plural(value, varients):
    varients = varients.split(",")
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        varient = 0
    elif 2 <= value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        varient = 1
    else:
        varient = 2

    return varients[varient]


@register.filter(name="markdown") # имя для фильтра, чтобы использовать {{ variable|markdown }}
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_posts():
    """
        Простой шаблонный тег, возвращающий число опубликованных постов
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
        Тег включения (обрабатывает предоставленные данные и возвращает прорисованный шаблон)
    """
    latest_posts = Post.published.order_by('-publish')[:count] # Отображать последние посты на боковой панели поста
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=3):
    """
        Получаем список всех постов с доп полем total_comments,
        в котором записано количество комментов для каждого поста,
        и сортируем по убываюнию по новому полю
    """
    return Post.published.annotate(
        total_comments=Count('comments') # annotate выполняет запрос из связной таблицы Comments и агрегирует (считает) колво комментов для каждого поста
    ).order_by('-total_comments')[:count]