from django.contrib import admin
from .models import Contact, Group

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'user', 'is_favorite', 'is_deleted')
    list_filter = ('is_favorite', 'is_deleted', 'created_at', 'user')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    date_hierarchy = 'created_at'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name',)
