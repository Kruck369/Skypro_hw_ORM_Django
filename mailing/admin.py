from django.contrib import admin

from mailing.models import Client, Newsletter, Message, DeliveryLog


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'middle_name', 'comment', 'author')
    search_fields = ('first_name', 'last_name')


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ('get_clients', 'message', 'time', 'frequency', 'status', 'author')
    list_filter = ('frequency', 'status', 'author')
    search_fields = ('client', 'time')

    def get_clients(self, obj):
        return ', '.join([client.email for client in obj.client.all()])
    get_clients.short_description = 'Клиенты'


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('subject', 'body', 'author',)
    search_fields = ('subject',)


@admin.register(DeliveryLog)
class AdminDeliveryLog(admin.ModelAdmin):
    list_display = ('message', 'timestamp', 'status', 'server_response')
    list_filter = ('status',)
    search_fields = ('timestamp', 'server_response')
