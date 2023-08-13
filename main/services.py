from django.core.cache import cache
from .models import Category


def get_cached_categories():
    cached_categories = cache.get('categories')
    if cached_categories is None:
        categories = Category.objects.all()
        cache.set('categories', categories)
        return categories
    return cached_categories
