from django.db import models
from core.models import Image


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.title