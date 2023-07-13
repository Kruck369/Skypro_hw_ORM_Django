from django.contrib import admin

from main.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
