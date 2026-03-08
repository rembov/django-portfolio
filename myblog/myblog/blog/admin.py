from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_at', 'moderated')
    list_filter = ('moderated', 'created_at')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(moderated=True)
    approve_comments.short_description = "Одобрить выбранные комментарии"