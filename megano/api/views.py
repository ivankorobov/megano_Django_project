from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from products.models import Product, Category
from django.core.serializers import serialize
import json
User = get_user_model()

def banners(request):
	products = Product.objects.order_by('pk').all()

	products_data = [
		{
			"id": product.pk,
			"category": product.category.title,
			"price": product.price,
			"count": product.count,
			"date": product.date,
			"title": product.title,
			"description": product.fullDescription,
			"freeDelivery": product.freeDelivery,
			"images": [
				{
					"src": str(product.image),
					"alt": "any alt text",
				}
			],
			"tags": [
				"string"
			],
			"reviews": 5,
			"rating": product.rating
		}
		for product in products.order_by('-price')[:3]
	]
	return JsonResponse(products_data, safe=False)

def categories(request):
	categories = Category.objects.order_by('pk').all()

	categories_data = [
		 {
			 "id": category.pk,
			 "title": category.title,
			 "image": {
				"src": str(category.image),
				 "alt": "Image alt string"
			 },
			 "subcategories": [
				 # {
					#  "id": str(category.parent),
					#  "title": str(category.parent),
					#  "image": {
					# 		"src": str(category.image),
					# 	 	"alt": "Image alt string"
					#  }
				 # }
			 ]
		 }
		for category in categories #if category.parent is None
	 ]
	return JsonResponse(categories_data, safe=False)


def catalog(request):
	products = Product.objects.order_by('pk').all()
	products_data = {
		 "items": [
			 {
				 "id": product.pk,
				 "category": product.category.title,
				 "price": product.price,
				 "count": product.count,
				 "date": product.date,
				 "title": product.title,
				 "description": product.fullDescription,
				 "freeDelivery": product.freeDelivery,
				 "images": [
					 {
						 "src": str(product.image),
						 "alt": "any alt text",
					 }
				 ],
				 "tags": [
					 "string"
				 ],
				 "reviews": 5,
				 "rating": product.rating
			 }
			 for product in products]
		 ,
		 "currentPage": 1,
		 "lastPage": 10
	 }
	return JsonResponse(products_data, safe=False)

def productsPopular(request):
	products = Product.objects.order_by('pk').all()

	products_data = [
		{
			"id": product.pk,
			"category": product.category.title,
			"price": product.price,
			"count": product.count,
			"date": product.date,
			"title": product.title,
			"description": product.fullDescription,
			"freeDelivery": product.freeDelivery,
			"images": [
				{
					"src": str(product.image),
					"alt": "any alt text",
				}
			],
			"tags": [
				"string"
			],
			"reviews": 5,
			"rating": product.rating
		}
		for product in products[:8]
	]
	return JsonResponse(products_data, safe=False)


def productsLimited(request):
	products = Product.objects.order_by('pk').all()

	products_data = [
		{
			"id": product.pk,
			"category": product.category.title,
			"price": product.price,
			"count": product.count,
			"date": product.date,
			"title": product.title,
			"description": product.fullDescription,
			"freeDelivery": product.freeDelivery,
			"images": [
				{
					"src": str(product.image),
					"alt": "any alt text",
				}
			],
			"tags": [
				"string"
			],
			"reviews": 5,
			"rating": product.rating
		}
		for product in products if product.limited_edition is True
	]
	return JsonResponse(products_data, safe=False)

def sales(request):
	products = Product.objects.order_by('pk').all()
	products_data = {
		"items": [
			{
				"id": product.pk,
				"category": product.category.title,
				"price": product.price,
				"count": product.count,
				"date": product.date,
				"title": product.title,
				"description": product.fullDescription,
				"freeDelivery": product.freeDelivery,
				"images": [
					{
						"src": str(product.image),
						"alt": "any alt text",
					}
				],
				"tags": [
					"string"
				],
				"reviews": 5,
				"rating": product.rating
			}
			for product in products]
		,
		"currentPage": 1,
		"lastPage": 10
	}
	return JsonResponse(products_data, safe=False)

def basket(request):
	if(request.method == "GET"):
		print('[GET] /api/basket/')
		data = [
			{
				"id": 123,
				"category": 55,
				"price": 500.67,
				"count": 12,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			},
			{
				"id": 124,
				"category": 55,
				"price": 201.675,
				"count": 5,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			},
			{
				"id": 125,
				"category": 55,
				"price": 201.675,
				"count": 5,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
						"alt": "hello alt",
					}
				],
				"tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
				],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

	elif (request.method == "POST"):
		body = json.loads(request.body)
		id = body['id']
		count = body['count']
		print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
		data = [
			{
				"id": id,
				"category": 55,
				"price": 500.67,
				"count": 13,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

	elif (request.method == "DELETE"):
		body = json.loads(request.body)
		id = body['id']
		print('[DELETE] /api/basket/')
		data = [
			{
			"id": id,
			"category": 55,
			"price": 500.67,
			"count": 11,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
			"reviews": 5,
			"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

def orders(request):
	if (request.method == "POST"):
		data = [
			{
			"id": 123,
			"category": 55,
			"price": 500.67,
			"count": 12,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

def signIn(request):
	if request.method == "POST":
		body = json.loads(request.body)
		username = body['username']
		password = body['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=500)

def signUp(request):
	user = User.objects.create_user("mir232", "lennon@thebeatles.com", "pass232")
	user.save()
	return HttpResponse(status=200)

def signOut(request):
	logout(request)
	return HttpResponse(status=200)

def product(request, id):
	data = {
		"id": 123,
		"category": 55,
		"price": 500.67,
		"count": 12,
		"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
		"title": "video card",
		"description": "description of the product",
		"fullDescription": "full description of the product",
		"freeDelivery": True,
		"images": [
				{
					"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
					"alt": "hello alt",
				}
		 ],
		 "tags": [
				{
					"id": 0,
					"name": "Hello world"
				}
		 ],
		"reviews": [
			{
				"author": "Annoying Orange",
				"email": "no-reply@mail.ru",
				"text": "rewrewrwerewrwerwerewrwerwer",
				"rate": 4,
				"date": "2023-05-05 12:12"
			}
		],
		"specifications": [
			{
				"name": "Size",
				"value": "XL"
			}
		],
		"rating": 4.6
	}
	return JsonResponse(data)

def tags(request):
	data = [
		{ "id": 0, "name": 'tag0' },
		{ "id": 1, "name": 'tag1' },
		{ "id": 2, "name": 'tag2' },
	]
	return JsonResponse(data, safe=False)

def productReviews(request, id):
	data = [
    {
      "author": "Annoying Orange",
      "email": "no-reply@mail.ru",
      "text": "rewrewrwerewrwerwerewrwerwer",
      "rate": 4,
      "date": "2023-05-05 12:12"
    },
    {
      "author": "2Annoying Orange",
      "email": "no-reply@mail.ru",
      "text": "rewrewrwerewrwerwerewrwerwer",
      "rate": 5,
      "date": "2023-05-05 12:12"
    },
	]
	return JsonResponse(data, safe=False)

def profile(request):
	if(request.method == 'GET'):
		data = {
			"fullName": "Annoying Orange",
			"email": "no-reply@mail.ru",
			"phone": "88002000600",
			"avatar": {
				"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
				"alt": "hello alt",
			}
		}
		return JsonResponse(data)

	elif(request.method == 'POST'):
		data = {
			"fullName": "Annoying Green",
			"email": "no-reply@mail.ru",
			"phone": "88002000600",
			"avatar": {
				"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
				"alt": "hello alt",
			}
		}
		return JsonResponse(data)

	return HttpResponse(status=500)

def profilePassword(request):
	return HttpResponse(status=200)

def orders(request):
	if(request.method == 'GET'):
		data = [
			{
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      },
			{
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      }
		]
		return JsonResponse(data, safe=False)

	elif(request.method == 'POST'):
		data = {
			"orderId": 123,
		}
		return JsonResponse(data)

	return HttpResponse(status=500)

def order(request, id):
	if(request.method == 'GET'):
		data = {
			"id": 123,
			"createdAt": "2023-05-05 12:12",
			"fullName": "Annoying Orange",
			"email": "no-reply@mail.ru",
			"phone": "88002000600",
			"deliveryType": "free",
			"paymentType": "online",
			"totalCost": 567.8,
			"status": "accepted",
			"city": "Moscow",
			"address": "red square 1",
			"products": [
				{
					"id": 123,
					"category": 55,
					"price": 500.67,
					"count": 12,
					"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
					"title": "video card",
					"description": "description of the product",
					"freeDelivery": True,
					"images": [
						{
						"src": "https://proprikol.ru/wp-content/uploads/2022/01/kartinki-vy-o-chem-17.jpg",
						"alt": "Image alt string"
						}
					],
					"tags": [
						{
						"id": 12,
						"name": "Gaming"
						}
					],
					"reviews": 5,
					"rating": 4.6
				},
			]
		}
		return JsonResponse(data)

	elif(request.method == 'POST'):
		data = { "orderId": 123 }
		return JsonResponse(data)

	return HttpResponse(status=500)

def payment(request, id):
	print('qweqwewqeqwe', id)
	return HttpResponse(status=200)

def avatar(request):
	if request.method == "POST":
# 		print(request.FILES["avatar"])
		return HttpResponse(status=200)