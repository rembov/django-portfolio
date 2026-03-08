from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    content = models.TextField('Содержание')
    image = models.ImageField('Изображение', upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField('Дата публикации', default=timezone.now)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author_name = models.CharField('Имя', max_length=100)
    author_email = models.EmailField('Email')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    moderated = models.BooleanField('Промодерирован', default=False)  # для возможности премодерации

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.post.title[:30]}'