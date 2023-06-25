from django.db import models
from django.contrib.auth.models import User
from products.models import Product

CART_SESSION_ID = 'cart'


class Cart(object):
    """Объект корзины в сессии"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            product_id = str(product.id)
            cart[product_id]["product_id"] = product_id
            cart[product_id]["price"] = float(product.price)
            cart[product_id]["total_price"] = (
                    cart[product_id]["price"] * cart[product_id]["quantity"]
            )

        sorted_cart = sorted(cart.values(), key=lambda item: item["product_id"])

        for item in sorted_cart:
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": float(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity >= self.cart[product_id]["quantity"]:
                del self.cart[product_id]
            else:
                self.cart[product_id]["quantity"] -= quantity
            self.save()

    def get_total_price(self):
        return sum(
            float(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='покупатель')
    date = models.DateField(auto_now_add=True, verbose_name='дата заказа')
    status = models.CharField(default='generated', max_length=50, null=False, blank=False)
    payment_type = models.CharField(default='online', max_length=30, null=False, blank=False)
    total_cost = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='итоговая цена')
    delivery_type = models.TextField(default='free', max_length=400, null=False, blank=False)
    city = models.CharField(default='Moscow', max_length=120, null=False, blank=False)
    address = models.CharField(default='red square 1', max_length=120, null=False, blank=False)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    count = models.PositiveIntegerField(default=1, null=False, blank=True, verbose_name='количество')


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ')
    name = models.TextField(default='fullname', max_length=120, null=False, blank=False)
    total_cost = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='оплатa')
