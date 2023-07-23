from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


@register.filter
def intspace(value):
    """Регистрируем кастомный фильтр для отображения суммы"""
    return intcomma(value).replace(',', ' ')
