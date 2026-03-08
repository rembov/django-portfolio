from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Item(models.Model):
    """Книга/фильм/игра"""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    year = models.PositiveIntegerField('Год выпуска')
    image = models.ImageField('Обложка', upload_to='items/', blank=True, null=True)
    average_rating = models.FloatField('Средний рейтинг', default=0, editable=False)

    class Meta:
        verbose_name = 'Элемент каталога'
        verbose_name_plural = 'Элементы каталога'
        ordering = ['-year']

    def __str__(self):
        return self.title

    def update_rating(self):
        """Пересчёт среднего рейтинга на основе оценок"""
        avg = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.average_rating = avg or 0
        self.save()

class Review(models.Model):
    """Отзыв и оценка пользователя"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('item', 'user')  # один пользователь может оставить только одну оценку

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.update_rating()