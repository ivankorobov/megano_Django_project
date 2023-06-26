from django.http import JsonResponse, HttpRequest
import json
import datetime
import pprint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import (
    Product,
    Category,
    SubCategory,
    ProductReviews,
    ProductSpecifications,
    Tag,
    ProductSale,
)
from orders.models import Order, ProductInOrder, Payment, Cart

User = get_user_model()


def banners(request):
    products = Product.objects.order_by("rating")
    i_tags = Product.objects.prefetch_related("tags").values("tags")

    data = [
        {
            "id": i_product.pk,
            "category": 1,
            "price": i_product.price,
            "count": i_product.count,
            "date": i_product.date,
            "title": i_product.name,
            "description": i_product.description,
            "freeDelivery": i_product.free_delivery,
            "images": [
                {
                    "src": "http://127.0.0.1:8000/media/{}".format(i_product.preview),
                    "alt": "any alt text",
                }
            ],
            "tags": ["string"],
            "reviews": i_product.reviewers,
            "rating": i_product.rating,
        }
        for i_product in products[:4]
    ]
    return JsonResponse(data, safe=False)


def categories(request):
    i_categories = Category.objects.all()
    data = [
        {
            "id": category.pk,
            "title": category.name,
            "image": {
                "src": "http://127.0.0.1:8000/media/{}".format(category.preview),
                "alt": "Image alt string",
            },
            "subcategories": [
                {
                    "id": subcategory.pk,
                    "title": subcategory.name,
                    "image": {
                        "src": "http://127.0.0.1:8000/media/{}".format(
                            subcategory.preview
                        ),
                        "alt": "Image alt string",
                    },
                }
                for subcategory in SubCategory.objects.filter(category=category.pk)
            ],
        }
        for category in i_categories
    ]
    return JsonResponse(data, safe=False)


def catalog(request):
    filter_catalog = request.GET
    pprint.pprint(filter_catalog)

    products = Product.objects.filter(
        name__icontains=filter_catalog["filter[name]"]
    ) & Product.objects.filter(
        price__range=(
            filter_catalog["filter[minPrice]"],
            filter_catalog["filter[maxPrice]"],
        )
    )
    if filter_catalog["filter[freeDelivery]"] == "true":
        products = products & Product.objects.filter(free_delivery=True)
    elif filter_catalog["filter[available]"] == "true":
        products = products & Product.objects.filter(count__gt=0)

    if "tags[]" in filter_catalog:
        filter_tags = request.GET.getlist("tags[]")

        for i_product in products:
            prod_tags = []

            for tag in i_product.tags.all():
                prod_tags.append(str(tag.pk))

            remove = True

            for tag in prod_tags:
                if tag in filter_tags:
                    remove = False

            if remove:
                products = products & Product.objects.exclude(pk=i_product.pk)

    sort = ""

    if filter_catalog["sort"] == "price":
        if filter_catalog["sortType"] == "inc":
            sort = "-price"
        else:
            sort = "price"

    elif filter_catalog["sort"] == "rating":
        if filter_catalog["sortType"] == "inc":
            sort = "-rating"
        else:
            sort = "rating"

    elif filter_catalog["sort"] == "reviews":
        if filter_catalog["sortType"] == "inc":
            sort = "-reviewers"
        else:
            sort = "reviewers"

    elif filter_catalog["sort"] == "date":
        if filter_catalog["sortType"] == "inc":
            sort = "-date"
        else:
            sort = "date"

    products = products.order_by(sort)

    data = {
        "items": [
            {
                "id": i_product.pk,
                "category": [
                    {"id": category.pk, "name": category.name}
                    for category in i_product.categories.all()
                ],
                "price": i_product.price,
                "count": i_product.count,
                "date": i_product.date,
                "title": i_product.name,
                "description": i_product.description,
                "freeDelivery": i_product.free_delivery,
                "images": [
                    {
                        "src": "http://127.0.0.1:8000/media/{}".format(
                            i_product.preview
                        ),
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": tag.pk,
                        "name": tag.name,
                    }
                    for tag in i_product.tags.all()
                ],
                "reviews": i_product.reviewers,
                "rating": i_product.rating,
            }
            for i_product in products
        ],
        "currentPage": 1,
        "lastPage": 3,
    }

    return JsonResponse(data)


def productsPopular(request):
    popular_products = Product.objects.filter(rating__gte=4).order_by("-rating")
    data = [
        {
            "id": i_product.pk,
            "category": [
                {"id": category.pk, "name": category.name}
                for category in i_product.categories.all()
            ],
            "price": i_product.price,
            "count": i_product.count,
            "date": i_product.date,
            "title": i_product.name,
            "description": i_product.description,
            "freeDelivery": i_product.free_delivery,
            "images": [
                {
                    "src": "http://127.0.0.1:8000/media/{}".format(i_product.preview),
                    "alt": "hello alt",
                }
            ],
            "tags": [
                {
                    "id": tag.pk,
                    "name": tag.name,
                }
                for tag in i_product.tags.all()
            ],
            "reviews": i_product.reviewers,
            "rating": i_product.rating,
        }
        for i_product in popular_products
    ]
    return JsonResponse(data, safe=False)


def productsLimited(request):
    lim_products = Product.objects.filter(limited=True).order_by("-rating")
    i_tags = Product.objects.prefetch_related("tags").values("tags")
    data = [
        {
            "id": i_product.pk,
            "category": [
                {"id": category.pk, "name": category.name}
                for category in i_product.categories.all()
            ],
            "price": i_product.price,
            "count": i_product.count,
            "date": i_product.date,
            "title": i_product.name,
            "description": i_product.description,
            "freeDelivery": i_product.free_delivery,
            "images": [
                {
                    "src": "http://127.0.0.1:8000/media/{}".format(i_product.preview),
                    "alt": "hello alt",
                }
            ],
            "tags": [{"id": tag.pk, "name": tag.name} for tag in i_product.tags.all()],
            "reviews": i_product.reviewers,
            "rating": i_product.rating,
        }
        for i_product in lim_products
    ]
    return JsonResponse(data, safe=False)


def sales(request):
    discounted_products = ProductSale.objects.filter(
        date_to__gte=datetime.datetime.now()
    ).order_by("date_to")

    data = {
        "items": [
            {
                "id": sale.product.pk,
                "price": sale.product.price,
                "salePrice": sale.sale_price,
                "dateFrom": sale.date_from.strftime("%m %d"),
                "dateTo": sale.date_to.strftime("%m %d"),
                "title": sale.product.name,
                "images": [
                    {
                        "src": "http://127.0.0.1:8000/media/{}".format(
                            sale.product.preview
                        ),
                        "alt": "hello alt",
                    }
                ],
            }
            for sale in discounted_products
        ],
        "currentPage": 1,
        "lastPage": 3,
    }
    return JsonResponse(data)


class CartDetailView(APIView):
    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            cart_items.append(
                {
                    "id": product.id,
                    "category": [
                        {"id": category.pk, "name": category.name}
                        for category in product.categories.all()
                    ],
                    "price": float(item["price"]),
                    "count": item["quantity"],
                    "date": product.date,
                    "title": product.name,
                    "description": product.description,
                    "freeDelivery": product.free_delivery,
                    "images": [
                        {
                            "src": "http://127.0.0.1:8000/media/{}".format(
                                product.preview
                            ),
                            "alt": "hello alt",
                        }
                    ],
                    "tags": [
                        {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                    ],
                    "reviews": product.reviewers,
                    "rating": product.rating,
                }
            )
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)
        product = Product.objects.get(id=product_id)

        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)


def orders(request):
    user_orders = Order.objects.filter(user=request.user.pk)
    if request.method == "GET":
        data = [
            {
                "id": order.pk,
                "createdAt": order.date,
                "fullName": order.user.username,
                "email": order.user.email,
                "phone": order.user.profile.phone,
                "deliveryType": order.delivery_type,
                "paymentType": order.payment_type,
                "totalCost": order.total_cost,
                "status": order.status,
                "city": order.city,
                "address": order.address,
                "products": [
                    {
                        "id": product.product.pk,
                        "category": [
                            {"id": category.pk, "name": category.name}
                            for category in product.product.categories.all()
                        ],
                        "price": product.product.price,
                        "count": product.product.count,
                        "date": product.product.date,
                        "title": product.product.name,
                        "description": product.product.description,
                        "freeDelivery": product.product.free_delivery,
                        "images": [
                            {
                                "src": "http://127.0.0.1:8000/media/{}".format(
                                    product.product.preview
                                ),
                                "alt": "Image alt string",
                            }
                        ],
                        "tags": [
                            {"id": tag.pk, "name": tag.name}
                            for tag in product.product.tags.all()
                        ],
                        "reviews": product.product.reviewers,
                        "rating": product.product.rating,
                    }
                    for product in ProductInOrder.objects.filter(order=order)
                ],
            }
            for order in user_orders
        ]

        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        data = json.loads(str(request.body, encoding="utf8"))

        order = Order.objects.create(
            user=request.user,
        )
        for product in data:
            ProductInOrder.objects.create(
                order=order,
                product=Product.objects.get(pk=product["id"]),
                count=product["count"],
            )

        data = {
            "orderId": order.pk,
        }
        return JsonResponse(data)

    return HttpResponse(status=500)


def signIn(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body["username"]
        password = body["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


def signUp(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        body = json.loads(request.body)
        username = body["username"]
        password = body["password"]
        new_user = User.objects.create_user(username=username, password=password)
        new_user.first_name = body["name"]
        new_user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, new_user)
        return HttpResponse(status=200)


def signOut(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponse(status=200)


def product(request, id):
    my_product = Product.objects.get(pk=id)
    reviews = ProductReviews.objects.filter(product=my_product.pk)

    i_tags = my_product.tags.all()
    i_category = my_product.categories.all()

    specifications = ProductSpecifications.objects.filter(product=my_product.pk)

    data = {
        "id": my_product.pk,
        "category": [
            {"id": category.pk, "name": category.name} for category in i_category
        ],
        "price": my_product.price,
        "count": my_product.count,
        "date": my_product.date,
        "title": my_product.name,
        "description": my_product.description,
        "fullDescription": my_product.full_description,
        "freeDelivery": my_product.free_delivery,
        "images": [
            {
                "src": "http://127.0.0.1:8000/media/{}".format(my_product.preview),
                "alt": "hello alt",
            }
        ],
        "tags": [{"id": tag.pk, "name": tag.name} for tag in i_tags],
        "reviews": [
            {
                "author": review.author,
                "email": review.author_email,
                "text": review.text,
                "rate": review.rate,
                "date": review.date,
            }
            for review in reviews
        ],
        "specifications": [
            {"name": spec.name, "value": spec.value} for spec in specifications
        ],
        "rating": my_product.rating,
    }
    return JsonResponse(data)


def tags(request):
    tag_list = Tag.objects.order_by("name").all()
    print(tag_list)
    data = [{"id": tag.pk, "name": tag.name} for tag in tag_list]
    return JsonResponse(data, safe=False)


def productReviews(request, id):
    body = json.loads(request.body)
    print(body)
    data = [
        {
            "author": body["author"],
            "email": body["email"],
            "text": body["text"],
            "rate": body["rate"],
            "date": datetime.datetime.now(),
        }
    ]
    ProductReviews.objects.create(
        product=Product.objects.get(pk=id),
        author=body["author"],
        author_email=body["email"],
        text=body["text"],
        rate=body["rate"],
        date=datetime.datetime.now(),
    )

    my_product = Product.objects.get(pk=id)
    my_product.reviewers += 1

    revs = ProductReviews.objects.filter(product=my_product.pk)

    rate = 0
    for i_rev in revs:
        rate += i_rev.rate
    rate /= len(revs)

    my_product.rating = rate

    my_product.save()

    return JsonResponse(data, safe=False)


def profile(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            avatar = request.user.profile.avatar

            data = {
                "fullName": "{username}".format(username=request.user.username),
                "email": "{email}".format(email=request.user.email),
                "phone": "{phone}".format(phone=request.user.profile.phone),
                "avatar": {
                    "src": "http://127.0.0.1:8000/media/{link}".format(link=avatar),
                    "alt": "hello alt",
                },
            }

            return JsonResponse(data)

        elif request.method == "POST":
            body = json.loads(request.body)
            request.user.username = body["fullName"]
            request.user.email = body["email"]
            request.user.profile.phone = body["phone"]
            avatar = request.user.profile.avatar

            data = {
                "fullName": request.user.username,
                "email": request.user.email,
                "phone": request.user.profile.phone,
                "avatar": {
                    "src": "http://127.0.0.1:8000/media/{link}".format(link=avatar),
                    "alt": "hello alt",
                },
            }

            request.user.save()
            return JsonResponse(data)

    else:
        return HttpResponse(status=500)


def profilePassword(request):
    body = json.loads(request.body)
    print(body["newPassword"])
    request.user.set_password(body["newPassword"])
    request.user.save()

    return HttpResponse(status=200)


def order(request, id):
    if request.method == "GET":
        order = Order.objects.get(pk=id)

        data = {
            "id": order.pk,
            "createdAt": order.date,
            "fullName": order.user.username,
            "email": order.user.email,
            "phone": order.user.profile.phone,
            "deliveryType": order.delivery_type,
            "paymentType": order.payment_type,
            "totalCost": order.total_cost,
            "status": order.status,
            "city": order.city,
            "address": order.address,
            "products": [
                {
                    "id": product.product.pk,
                    "category": [
                        {"id": category.pk, "name": category.name}
                        for category in product.product.categories.all()
                    ],
                    "price": product.product.price,
                    "count": product.count,
                    "date": product.product.date,
                    "title": product.product.name,
                    "description": product.product.description,
                    "freeDelivery": product.product.free_delivery,
                    "images": [
                        {
                            "src": "http://127.0.0.1:8000/media/{}".format(
                                product.product.preview
                            ),
                            "alt": "Image alt string",
                        }
                    ],
                    "tags": [
                        {"id": tag.pk, "name": tag.name}
                        for tag in product.product.tags.all()
                    ],
                    "reviews": product.product.reviewers,
                    "rating": product.product.rating,
                }
                for product in ProductInOrder.objects.filter(order=order)
            ],
        }
        return JsonResponse(data)

    elif request.method == "POST":
        data = json.loads(str(request.body, encoding="utf8"))
        order = Order.objects.get(pk=data["orderId"])
        order.status = "approved"
        order.total_cost = data["basketCount"]["price"]
        order.city = data["city"]
        order.address = data["address"]

        if data["paymentType"] == "online":
            order.payment_type = "card online"
        else:
            order.payment_type = "online from account"

        if data["deliveryType"] == "express":
            order.delivery_type = "paid + 10 by express delivery."
            order.total_cost += 10

        order_products = ProductInOrder.objects.filter(order=order)
        for product in order_products:
            if not product.product.free_delivery:
                order.total_cost += 5
                order.delivery_type += "\n+ 5 for paid delivery of {product}".format(
                    product=product.product.name
                )

        order.save()

        data = {"orderId": data["orderId"]}
        return JsonResponse(data)

    return HttpResponse(status=500)


def payment(request, id):
    order = Order.objects.get(pk=id)
    body = json.loads(request.body)

    products = ProductInOrder.objects.filter(order=order)
    Payment.objects.create(order=order, name=body["name"], total_cost=order.total_cost)

    order.status = "paid, in delivery"
    order.save()

    for order_product in products:
        sold_product = Product.objects.get(pk=order_product.product.pk)
        sold_product.sell(order_product.count)
        sold_product.save()

    return HttpResponse(status=200)


def avatar(request):
    if request.method == "POST":
        request.user.profile.avatar = request.FILES["avatar"]
        request.user.save()
        return HttpResponse(status=200)
