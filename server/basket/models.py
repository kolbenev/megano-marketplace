from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField, ManyToManyField

from product.models import Product


class Basket(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    products = ManyToManyField(Product, blank=True)
