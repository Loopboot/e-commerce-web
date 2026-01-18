from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.manage_products, name='manage_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/update/<int:order_id>/', views.update_order_status_view, name='update_order_status'),
    path('users/', views.manage_users, name='manage_users'),
]
