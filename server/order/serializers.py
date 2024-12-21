from rest_framework import serializers

from product.serializers import ProductShortSerializers
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name="get_product")

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def get_product(self, obj):
        products = obj.products.all()
        return ProductShortSerializers(products, many=True).data
