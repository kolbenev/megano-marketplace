from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="basket")
    session_key = models.CharField(max_length=255, null=True, blank=True, unique=True)
    items = models.ManyToManyField(Product, through="BasketItem")

    def __str__(self):
        if self.user:
            return f"Basket of {self.user.username}"
        return f"Basket for session {self.session_key}"

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="basket_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"
