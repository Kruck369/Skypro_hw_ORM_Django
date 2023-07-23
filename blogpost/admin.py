from django.contrib import admin

from blogpost.models import BlogPost


@admin.register(BlogPost)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'content',)
