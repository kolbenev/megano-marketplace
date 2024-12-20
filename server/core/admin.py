from django.contrib import admin

from core.models import Tag


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
