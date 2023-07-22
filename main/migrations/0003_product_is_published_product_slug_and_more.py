# Generated by Django 4.2.3 on 2023-07-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='опубликован'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='product',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='просмотры'),
        ),
    ]
