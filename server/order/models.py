from django.db import models
from django.core.validators import MinValueValidator

from product.models import Product


class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    deliveryType = models.CharField(max_length=20)
    paymentType = models.CharField(max_length=20)
    totalCost = models.DecimalField(
        decimal_places=2, max_digits=20, validators=[MinValueValidator(0)], default=0
    )
    status = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name="orders")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return str(self.id)
