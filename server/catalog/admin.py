from django.contrib import admin
from catalog.models import Category, CategoryImage


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ("id", "src", "alt")
    search_fields = ("alt",)
    list_per_page = 20
    ordering = ("id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent", "image")
    search_fields = ("title", "parent__title")
    list_filter = ("parent",)
    autocomplete_fields = ("parent", "image")
    list_per_page = 20
    ordering = ("id",)
