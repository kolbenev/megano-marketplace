from rest_framework import serializers

from product.models import Product
from tags.serializers import TagSerializer
from product.serializers import ProductImageSerializers


class ProductInBasketSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name="get_product_images")
    tags = serializers.SerializerMethodField(method_name="get_tags")
    reviews = serializers.IntegerField(source="reviews_count", read_only=True)
    rating = serializers.FloatField(source="average_rating", read_only=True)
    count = serializers.SerializerMethodField(method_name="get_count")

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

    def get_count(self, obj):
        basket_item = self.context.get("basket_items", {}).get(obj.id)
        return basket_item.quantity if basket_item else 0

    def get_tags(self, obj):
        return [TagSerializer(tag).data for tag in obj.tags.all()]

    def get_product_images(self, obj):
        return [ProductImageSerializers(image).data for image in obj.images.all()]
