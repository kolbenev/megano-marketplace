# Generated by Django 5.1.4 on 2024-12-19 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_alter_product_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sale",
            options={"verbose_name": "Sale", "verbose_name_plural": "Sales"},
        ),
    ]
