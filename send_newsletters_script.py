import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from mailing.models import Newsletter, DeliveryLog


def send_newsletters():
    now = timezone.localtime(timezone.now())

    started_newsletters = Newsletter.objects.filter(status=Newsletter.STARTED)

    for newsletter in started_newsletters:
        if newsletter.time > now.time():
            continue

        last_delivery = DeliveryLog.objects.filter(
            message=newsletter.message,
            status=DeliveryLog.SUCCESS
        ).order_by('-timestamp').first()

        if last_delivery:
            time_since_last_delivery = now - last_delivery.timestamp
        else:
            time_since_last_delivery = timedelta()

        if newsletter.frequency == Newsletter.DAILY and time_since_last_delivery >= timedelta(days=1):
            send_to_clients(newsletter)
        elif newsletter.frequency == Newsletter.WEEKLY and time_since_last_delivery >= timedelta(weeks=1):
            send_to_clients(newsletter)
        elif newsletter.frequency == Newsletter.MONTHLY and time_since_last_delivery >= timedelta(days=30):
            send_to_clients(newsletter)
        else:
            send_to_clients(newsletter)


def send_to_clients(newsletter):
    clients = newsletter.client.all()
    message = newsletter.message

    for client in clients:
        try:
            send_mail(
                message.subject,
                message.body,
                'tripicto369@gmail.com',
                [client.email],
                fail_silently=False,
            )

            delivery_log = DeliveryLog.objects.create(
                message=message,
                status=DeliveryLog.SUCCESS,
            )

            newsletter.status = Newsletter.COMPLETED
            newsletter.save()

        except Exception as e:
            delivery_log = DeliveryLog.objects.create(
                message=message,
                status=DeliveryLog.FAILED,
                server_response=str(e)
            )

            newsletter.status = Newsletter.COMPLETED
            newsletter.save()


if __name__ == '__main__':
    send_newsletters()
