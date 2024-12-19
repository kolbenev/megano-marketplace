from django.contrib.auth.models import User
from django.db import models

from catalog.models import Category
from core.models import Tag


class ProductImage(models.Model):
    src = models.ImageField(upload_to="products/images")
    alt = models.CharField(max_length=100)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    rate = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    full_description = models.TextField(blank=True, null=True)
    free_delivery = models.BooleanField(default=False)
    images = models.ManyToManyField(ProductImage, related_name="products")
    tags = models.ManyToManyField(Tag, blank=True)
    reviews = models.ManyToManyField(Review, blank=True)
    specifications = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title


class Sale(models.Model):
    product = models.ForeignKey(Product, related_name="sales", on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return self.title
