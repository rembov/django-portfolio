from django.contrib import admin
from .models import Word, Achievement, UserAchievement

admin.site.register(Word)
admin.site.register(Achievement)
admin.site.register(UserAchievement)