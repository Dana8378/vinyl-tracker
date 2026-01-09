from django.contrib import admin
from .models import Genre, RecordCondition, VinylRecord

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(RecordCondition)
class RecordConditionAdmin(admin.ModelAdmin):
    list_display = ['grade', 'description']


@admin.register(VinylRecord)
class VinylRecordAdmin(admin.ModelAdmin):
    list_display = ['artist', 'title', 'year', 'genre', 'estimated_value', 'user']
    list_filter = ['genre', 'year', 'condition']
    search_fields = ['artist', 'title']
