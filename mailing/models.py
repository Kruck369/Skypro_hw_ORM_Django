from django.db import models
from django.contrib.auth import get_user_model
from main.models import NULLABLE


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='контактная почта')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='отчество')
    comment = models.TextField(blank=True, verbose_name='комментарий')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return str(self.email) + ": " + self.last_name[:1] + "." + self.first_name[:1] + "." + self.middle_name[:1] + "."

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ('first_name',)


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='тема')
    body = models.TextField(verbose_name='сообщение')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ('newsletter',)


class Newsletter(models.Model):
    DAILY = "ED"
    WEEKLY = "EW"
    MONTHLY = "EM"
    CREATED = "CR"
    STARTED = "ST"
    COMPLETED = "CMP"
    client = models.ManyToManyField(Client, verbose_name='клиент')
    time = models.TimeField(verbose_name='время рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    frequency_choices = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]
    frequency = models.CharField(max_length=20, choices=frequency_choices, verbose_name='частота рассылки')
    status_choices = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Заврешена"),
    ]
    status = models.CharField(default=CREATED, max_length=10, choices=status_choices, verbose_name='статус рассылки')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='автор')

    def __str__(self):
        return f"{self.client}: {self.time}, {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ('status',)


class DeliveryLog(models.Model):
    SUCCESS = "SC"
    FAILED = "FD"
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    timestamp = models.DateTimeField(auto_now_add=True)
    status_choices = [
        (SUCCESS, 'Успешно'),
        (FAILED, 'Провалено')
    ]
    status = models.CharField(max_length=15, choices=status_choices, verbose_name='статус')
    server_response = models.TextField(verbose_name='ответ от сервера', **NULLABLE)

    def __str__(self):
        return f"{self.timestamp}: {self.status}"

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылки"
        ordering = ('status',)


class Meta:
    permissions = [
        ("can_create_newsletters", "Может создавать рассылки"),
    ]
