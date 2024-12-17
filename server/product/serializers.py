from rest_framework import serializers

from product.models import Product


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "category", "price", "count",
            "date", "title", "description",
            "freeDelivery", "images", "tags",
            "reviews", "rating"
        ]


class ProductFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "category", "price", "count",
            "date", "title", "description",
            "fullDescription", "freeDelivery",
            "images", "tags", "reviews", "rating",
            "specifications",
        ]
