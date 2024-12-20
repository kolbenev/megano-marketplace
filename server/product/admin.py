from django.contrib import admin

from django.contrib import admin
from .models import ProductImage, Review, Product, Sale


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "src", "alt")
    search_fields = ("alt",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "email", "rate", "date")
    list_filter = ("rate", "date")
    search_fields = ("author__username", "email", "text")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "count", "freeDelivery", "date")
    list_filter = ("category", "freeDelivery", "date")
    search_fields = ("title", "description", "fullDescription")
    filter_horizontal = ("images", "tags", "reviews")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "product", "salePrice", "dateFrom", "dateTo")
    list_filter = ("dateFrom", "dateTo")
    search_fields = ("title", "product__title")
