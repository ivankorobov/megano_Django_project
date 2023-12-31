# Generated by Django 4.1.7 on 2023-06-25 08:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=120, verbose_name="название")),
                (
                    "short_desc",
                    models.TextField(
                        blank=True, null=True, verbose_name="краткое описание"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.category_preview_directory_path,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=120, verbose_name="название")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=8, verbose_name="цена"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="краткое описание"),
                ),
                ("date", models.DateField(auto_now_add=True, verbose_name="дата")),
                (
                    "full_description",
                    models.TextField(blank=True, verbose_name="полное описание"),
                ),
                (
                    "free_delivery",
                    models.BooleanField(
                        default=True, verbose_name="бесплатная доставка"
                    ),
                ),
                (
                    "count",
                    models.IntegerField(default=0, verbose_name="количество товара"),
                ),
                (
                    "limited",
                    models.BooleanField(
                        default=False, verbose_name="лимитированный товар"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.product_preview_directory_path,
                    ),
                ),
                (
                    "reviewers",
                    models.IntegerField(default=0, verbose_name="количество отзывов"),
                ),
                (
                    "rating",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=3,
                        verbose_name="рейтинг",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="categories", to="products.category"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=120, verbose_name="название")),
                (
                    "short_desc",
                    models.TextField(
                        blank=True, null=True, verbose_name="краткое описание"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubCategory",
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
                ("name", models.CharField(max_length=120, verbose_name="название")),
                (
                    "short_desc",
                    models.TextField(
                        blank=True, null=True, verbose_name="краткое описание"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.category_preview_directory_path,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategory",
                        to="products.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductSpecifications",
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
                ("name", models.CharField(max_length=80)),
                ("value", models.TextField(verbose_name="значение")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specifications",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductSale",
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
                (
                    "sale_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        verbose_name="цена со скидкой",
                    ),
                ),
                (
                    "date_from",
                    models.DateField(auto_now_add=True, verbose_name="дата начала"),
                ),
                ("date_to", models.DateField(default=datetime.timedelta(days=5))),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                        verbose_name="скидка",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductReviews",
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
                ("author", models.CharField(max_length=120)),
                ("author_email", models.CharField(blank=True, max_length=120)),
                ("text", models.TextField(blank=True, null=True, verbose_name="отзыв")),
                (
                    "rate",
                    models.PositiveIntegerField(blank=True, verbose_name="рейтинг"),
                ),
                ("date", models.DateField(auto_now_add=True, verbose_name="дата")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                (
                    "image",
                    models.ImageField(
                        upload_to=products.models.product_images_directory_path
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="subcategories",
            field=models.ManyToManyField(
                related_name="subcategories", to="products.subcategory"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(related_name="tags", to="products.tag"),
        ),
    ]
