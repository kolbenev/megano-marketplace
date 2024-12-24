from rest_framework import serializers

from order.models import Order
from product.serializers import ProductShortSerializers


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
