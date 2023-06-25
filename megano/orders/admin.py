from django.contrib import admin
from .models import Order, ProductInOrder, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'status', 'payment_type', 'total_cost', 'city', 'address', ]


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'count',
    ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'name',
        'total_cost',
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Payment, PaymentAdmin)