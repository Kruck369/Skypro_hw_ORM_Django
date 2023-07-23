from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='blogpost/', verbose_name='превью', **NULLABLE)
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)
    date_of_creation = models.DateTimeField(verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}: {self.content}'

    class Meta:
        verbose_name = 'Блог пост'
        verbose_name_plural = 'Блог посты'
        ordering = ('id',)
