from django.contrib import admin

from main.models import Product, Category, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_number', 'version_name', 'is_active', 'product')
    list_filter = ('product',)
