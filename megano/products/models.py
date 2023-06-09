from django.db import models


def product_image_directory_path(instance: 'ProductImage', filename):
    """
    Получение пути для сохранения изображения продукта
    """

    return f'products/images/{instance.product.pk}/{filename}'


def category_image_directory_path(instance: 'CategoryIcons', filename):
    """
    Получение пути для загрузки иконки категории
    """

    if instance.category.parent:
        return f'products/icons/{instance.category.parent}/{instance.category}/{filename}'
    else:
        return f'products/icons/{instance.category}/{filename}'


class Category(models.Model):
    """
    Модель категории
    """
    title = models.CharField(max_length=128, db_index=True, verbose_name='название')
    active = models.BooleanField(default=False, verbose_name='активная')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='subcategories',
                               verbose_name='родитель')
    favourite = models.BooleanField(default=False, verbose_name='избранная категория')
    image = models.FileField(upload_to=category_image_directory_path, verbose_name='изображение', null=True)

    class Meta:
        ordering = ["title", "pk"]
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def href(self):
        """
        Получение ссылки
        """

        return f'/catalog/{self.pk}'

    def __str__(self):
        return self.title


class CategoryIcons(models.Model):
    """
    Модель иконки категории
    """

    src = models.FileField(upload_to=category_image_directory_path, max_length=500, verbose_name='иконка')
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='images', verbose_name='категория',
                                    blank=True, null=True)

    class Meta:
        ordering = ["pk"]
        verbose_name = "иконка категории"
        verbose_name_plural = "иконки категорий"

    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории
        """

        return self.category.title

    def __str__(self):
        return f'{self.pk}-я иконка'


class Product(models.Model):
    """
    Модель продукта
    """
    title = models.CharField(max_length=128, verbose_name='название')
    price = models.DecimalField(max_digits=10, db_index=True, decimal_places=2, default=0, verbose_name='цена')
    count = models.PositiveIntegerField(default=0, verbose_name='количество')
    fullDescription = models.TextField(default='', verbose_name='полное описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='products', verbose_name='категория')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченная серия')
    freeDelivery = models.BooleanField(default=False, verbose_name='бесплатная доставка')
    rating = models.PositiveIntegerField()
    active = models.BooleanField(default=False, verbose_name='активный')
    image = models.FileField(upload_to=product_image_directory_path, verbose_name='изображение', null=True)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def href(self):
        return f"/product/{self.pk}"

    def get_reviews_count(self):
        return self.reviews.count()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    Модель изображения продукта
    """

    image = models.FileField(upload_to=product_image_directory_path, verbose_name='изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='продукт')

    class Meta:
        ordering = ["pk"]
        verbose_name = "изображение продукта"
        verbose_name_plural = "изображения продуктов"

    def src(self):
        """
        Получаем ссылку на изображение.
        """

        return self.image

    def __str__(self):
        return f'/{self.image}'


class Tag(models.Model):
    """
    Модель тега
    """
    name = models.CharField(max_length=128, default='', db_index=True, verbose_name='имя')
    product = models.ManyToManyField(Product, related_name='tags', verbose_name='тэг')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        indexes = [
            models.Index(fields=['name'], name='name_ind')
        ]

    def __str__(self):
        return self.name


class Specification(models.Model):
    """
    Модель всех характеристик продуктов
    """

    name = models.CharField(max_length=128, default='', verbose_name='название')
    category = models.ManyToManyField(Category, related_name='specifications',
                                      verbose_name='категория')

    class Meta:
        verbose_name = 'характеристика'
        verbose_name_plural = 'характеристики'

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    Модель характеристик конкретного продукта
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='specifications',
                                verbose_name='продукт')
    name = models.ForeignKey(Specification, on_delete=models.PROTECT, related_name='specification_name',
                             verbose_name='название')
    value = models.CharField(max_length=256, default='', verbose_name='значение')

    class Meta:
        verbose_name = 'характеристика продукта'
        verbose_name_plural = 'характеристики продуктов'


class Reviews(models.Model):
    """
    Модель отзывов о продукте
    """

    author = models.CharField(max_length=128, verbose_name='автор')
    email = models.EmailField(max_length=254)
    text = models.TextField(verbose_name='текст')
    rate = models.PositiveSmallIntegerField(blank=False, default=5, verbose_name='оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='reviews',
                                verbose_name='продукт')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text


class Sale(models.Model):
    """
    Модель продуктов со скидками
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name='продукт')
    salePrice = models.DecimalField(max_digits=10, db_index=True, decimal_places=2, default=0, verbose_name='цена по скидке')
    dateFrom = models.DateField(default='', verbose_name='старт продаж')
    dateTo = models.DateField(verbose_name='окончание продаж', blank=True, null=True)

    class Meta:
        verbose_name = 'распродажа'
        verbose_name_plural = 'распродажи'

    def price(self):
        """
        Получение первоначальной цены продукта
        """

        return self.product.price

    def images(self):
        """
        Получение изображений продукта
        """

        return self.product.images

    def title(self):
        """
        Получение названия продукта
        """

        return self.product.title

    def href(self):
        """
        Получение ссылки на детальную страницу продукта
        """

        return f'/product/{self.product.pk}'

    def __str__(self):
        return self.product.title

