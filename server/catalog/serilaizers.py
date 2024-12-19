from typing import List, Dict

from rest_framework import serializers

from catalog.models import CategoryImage, Category


class ImageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ["src", "alt"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(
        method_name="getter_subcategories"
    )
    image = serializers.SerializerMethodField(method_name="getter_images")

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]

    def getter_images(self, obj):
        return ImageCategorySerializer(obj.image).data

    def getter_subcategories(self, obj: Category) -> List[Dict]:
        data = [
            {
                "id": obj.id,
                "title": obj.title,
                "image": ImageCategorySerializer(obj.image).data,
            }
            for obj in obj.subcategories.all()
        ]

        return data
