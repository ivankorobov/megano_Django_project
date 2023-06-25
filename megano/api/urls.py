from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    path('banners', views.banners),
    path('categories', views.categories),
    path('catalog', views.catalog),

    path('products/popular', views.productsPopular),
    path('products/limited', views.productsLimited),
    path('sales', views.sales),

    path('basket', views.CartDetailView.as_view()),
    path('orders', views.orders),
    path('order/<int:id>', views.order),
    path('payment/<int:id>', views.payment),

    path('sign-in', views.signIn),
    path('sign-up', views.signUp),
    path('sign-out', views.signOut),

    path('product/<int:id>', views.product),
    path('product/<int:id>/reviews', views.productReviews),
    path('tags', views.tags),

    path('profile', views.profile),
    path('profile/password', views.profilePassword),
    path('profile/avatar', views.avatar),
]

# if settings.DEBUG:
#     urlpatterns.extend(
#         static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     )