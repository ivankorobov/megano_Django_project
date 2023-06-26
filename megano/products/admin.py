from django.contrib import admin


from django.contrib import admin
from .models import (
    Product,
    Tag,
    ProductReviews,
    ProductSpecifications,
    Category,
    SubCategory,
    ProductSale,
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "limited", "count", "preview"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "short_desc"]


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ["product", "author", "author_email", "text", "rate", "date"]


class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = ["name", "value"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "short_desc"]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "short_desc"]


class ProductSaleAdmin(admin.ModelAdmin):
    list_display = ["product", "sale_price", "date_from", "date_to"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "date",
        "status",
        "payment_type",
        "total_cost",
        "city",
        "address",
    ]


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "product",
        "count",
    ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "name",
        "total_cost",
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ProductReviews, ReviewsAdmin)
admin.site.register(ProductSpecifications, ProductSpecificationsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(ProductSale, ProductSaleAdmin)
