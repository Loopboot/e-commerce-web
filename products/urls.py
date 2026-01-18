from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
]
