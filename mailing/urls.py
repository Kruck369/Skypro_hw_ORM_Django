from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

from mailing.apps import MailingConfig
from mailing.views import NewsletterListView, NewsletterCreateView, NewsletterUpdateView, NewsletterDetailView, \
    NewsletterDeleteView, MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', NewsletterListView.as_view(), name='index'),
    path('create/', NewsletterCreateView.as_view(), name='create'),
    path('edit/<int:pk>', NewsletterUpdateView.as_view(), name='edit'),
    path('newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter'),
    path('delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete'),
    path('newsletter/<int:pk>/start/', views.start_newsletter, name='start_newsletter'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>', cache_page(10)(MessageDetailView.as_view()), name='message_detail'),
    path('message/edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>', cache_page(10)(ClientDetailView.as_view()), name='client_detail'),
    path('client/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
]
