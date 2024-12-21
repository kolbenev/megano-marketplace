# Generated by Django 5.1.4 on 2024-12-21 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("fullName", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("deliveryType", models.CharField(max_length=20)),
                ("paymentType", models.CharField(max_length=20)),
                (
                    "totalCost",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=20,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("status", models.CharField(max_length=20)),
                ("city", models.CharField(max_length=20)),
                ("address", models.CharField(max_length=100)),
                (
                    "products",
                    models.ManyToManyField(related_name="orders", to="product.product"),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
    ]
