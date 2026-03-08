from django.contrib import admin
from .models import Service, ContactRequest, SiteSettings

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'order')
    list_editable = ('order',)  # можно менять порядок прямо в списке
    search_fields = ('name',)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # чтобы нельзя было создать несколько записей
    def has_add_permission(self, request):
        return False if SiteSettings.objects.exists() else True