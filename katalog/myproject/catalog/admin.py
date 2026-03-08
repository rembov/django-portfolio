from django.contrib import admin
from .models import Category, Item, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'average_rating')
    list_filter = ('category', 'year')
    search_fields = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'rating', 'created_at')