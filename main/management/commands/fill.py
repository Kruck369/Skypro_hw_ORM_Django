from django.core.management import BaseCommand

from main.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Категория 6', 'description': 'Описание категории 6'},
            {'name': 'Категория 7', 'description': 'Описание категории 7'},
            {'name': 'Категория 8', 'description': 'Описание категории 8'},
            {'name': 'Категория 9', 'description': 'Описание категории 9'},
            {'name': 'Категория 10', 'description': 'Описание категории 10'},
            {'name': 'Категория 11', 'description': 'Описание категории 11'},
        ]

        categories_for_create = []
        for category in category_list:
            categories_for_create.append(
                Category(**category)
            )

        Category.objects.all().delete()
        Category.objects.bulk_create(categories_for_create)
