from rest_framework import serializers

from tags.serializers import TagSerializer
from product.models import Product, Sale, ProductImage, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name="get_author")

    class Meta:
        model = Review
        fields = [
            "author",
            "email",
            "text",
            "rate",
            "date",
        ]

    def get_author(self, obj):
        return obj.author.username


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


class ProductFullSerializers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name="get_product_images")
    tags = serializers.SerializerMethodField(method_name="get_tags")
    reviews = serializers.SerializerMethodField(method_name="get_reviews")
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
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_product_images(self, obj):
        return [image.src.url for image in obj.images.all()]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_reviews(self, obj):
        return [ReviewSerializer(review).data for review in obj.reviews.all()]


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
