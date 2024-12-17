from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    src = models.ImageField(upload_to='images/')
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.src