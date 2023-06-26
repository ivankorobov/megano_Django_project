from django.db import models
import datetime


def product_preview_directory_path(instance: "Product", filename: str):
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def category_preview_directory_path(instance: "Category", filename: str):
    return "categories/category_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def subcategory_preview_directory_path(instance: "SubCategory", filename: str):
    return "subcategories/subcategory_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class Tag(models.Model):
    name = models.CharField(max_length=120, verbose_name="название")
    short_desc = models.TextField(
        null=True, blank=True, verbose_name="краткое описание"
    )


class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name="название")
    short_desc = models.TextField(
        null=True, blank=True, verbose_name="краткое описание"
    )
    preview = models.ImageField(
        null=True, blank=True, upload_to=category_preview_directory_path
    )


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategory"
    )
    name = models.CharField(max_length=120, verbose_name="название")
    short_desc = models.TextField(
        null=True, blank=True, verbose_name="краткое описание"
    )
    preview = models.ImageField(
        null=True, blank=True, upload_to=category_preview_directory_path
    )


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name="название")
    price = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, verbose_name="цена"
    )
    description = models.TextField(
        null=False, blank=True, verbose_name="краткое описание"
    )
    date = models.DateField(auto_now_add=True, verbose_name="дата")
    full_description = models.TextField(
        null=False, blank=True, verbose_name="полное описание"
    )
    free_delivery = models.BooleanField(
        default=True, verbose_name="бесплатная доставка"
    )
    count = models.IntegerField(null=False, default=0, verbose_name="количество товара")
    limited = models.BooleanField(default=False, verbose_name="лимитированный товар")
    preview = models.ImageField(
        null=True, blank=True, upload_to=product_preview_directory_path
    )
    tags = models.ManyToManyField(Tag, related_name="tags")
    categories = models.ManyToManyField(Category, related_name="categories")
    subcategories = models.ManyToManyField(SubCategory, related_name="subcategories")
    reviewers = models.IntegerField(default=0, verbose_name="количество отзывов")
    rating = models.DecimalField(
        default=0, max_digits=3, decimal_places=2, verbose_name="рейтинг"
    )

    def sell(self, count_in_order):
        self.count -= count_in_order


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class ProductReviews(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.CharField(max_length=120, null=False, blank=False)
    author_email = models.CharField(max_length=120, null=False, blank=True)
    text = models.TextField(null=True, blank=True, verbose_name="отзыв")
    rate = models.PositiveIntegerField(null=False, blank=True, verbose_name="рейтинг")
    date = models.DateField(auto_now_add=True, verbose_name="дата")


class ProductSpecifications(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(max_length=80, null=False, blank=False)
    value = models.TextField(null=False, blank=False, verbose_name="значение")


class ProductSale(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="скидка"
    )
    sale_price = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, verbose_name="цена со скидкой"
    )
    date_from = models.DateField(auto_now_add=True, verbose_name="дата начала")
    date_to = models.DateField(default=datetime.timedelta(days=5))
