from django.contrib.auth.models import User
from django.db import models


class CategoryImage(models.Model):
    src = models.ImageField(upload_to="media/images/categories/")
    alt = models.CharField(max_length=100)


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ForeignKey(
        CategoryImage,
        related_name="category",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "Catalogs"
        verbose_name = "Catalog"

    def __str__(self):
        return self.title
