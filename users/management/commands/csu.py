from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='reka_931@mail.ru',
            first_name='Admin',
            last_name='Kruck',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('65123891Sad@')
        user.save()
