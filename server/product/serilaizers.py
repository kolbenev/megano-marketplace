from core.serilaizers import TagSerializer
from product.models import Product, Sale, ProductImage
from rest_framework import serializers


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["src", "alt"]


class ProductShortSerializers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name="get_product_images")
    tags = serializers.SerializerMethodField(method_name="get_tags")
    reviews = serializers.IntegerField(source="reviews_count", read_only=True)
    rating = serializers.FloatField(source="average_rating", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_tags(self, obj):
        return [TagSerializer(tag).data for tag in obj.tags.all()]

    def get_product_images(self, obj):
        return [ProductImageSerializers(image).data for image in obj.images.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("rating") is None:
            representation["rating"] = 0.0
        return representation


class SaleSerializers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = [
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        ]

    def get_images(self, obj):
        return [image.src for image in obj.product.images.all()]

    def get_price(self, obj):
        return obj.product.price
