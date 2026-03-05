from django.contrib import admin
from .models import FavouriteVideo

@admin.register(FavouriteVideo)
class FavouriteVideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'url', 'created_at']
    list_filter  = ['user']
    search_fields = ['name', 'url']
