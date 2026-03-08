from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    CATEGORY_CHOICES = [
        ('alphabet', 'Алфавит'),
        ('professions', 'Профессии'),
        ('animals', 'Животные'),
        ('colors', 'Цвета'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    # Поле image больше не нужно – используем эмодзи в шаблоне

    def __str__(self):
        return f"{self.word} ({self.category})"

class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True)   # 'game', 'grammar_am', ...
    name = models.CharField(max_length=100)               # 'Игрок', 'Знаток to be'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')