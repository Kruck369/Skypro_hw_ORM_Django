from django import template

register = template.Library()


@register.simple_tag
def mediapath(image_path):
    """Регистрируем кастомный тег для отображения изображений"""
    return '/media/' + str(image_path)


@register.filter
def mediapath(image_path):
    """Регистрируем кастомный фильтр для отображения изображений"""
    return f"/media/{image_path}"
