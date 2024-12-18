from rest_framework import serializers
from .models import Product, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'count', 'rating', 'free_delivery', 'image', 'tags', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories', 'products']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data
