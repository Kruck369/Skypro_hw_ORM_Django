from django.urls import path

from blogpost.apps import BlogpostConfig
from blogpost.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostDeleteView, BlogPostUpdateView

app_name = BlogpostConfig.name

urlpatterns = [
    path('list/', BlogPostListView.as_view(), name='list'),
    path('blogpost/<int:pk>', BlogPostDetailView.as_view(), name='blogpost'),
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('delete/<int:pk>', BlogPostDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>', BlogPostUpdateView.as_view(), name='edit')
]
