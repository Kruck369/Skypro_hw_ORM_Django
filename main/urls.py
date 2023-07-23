from django.urls import path

from main.apps import MainConfig
from main.views import ProductDetailView, ProductListView, ProductCreateView, ProductDeleteView, ProductUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit'),
]
