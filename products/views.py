from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .services import ProductService
from users.services import CartService

def homepage(request):
    """Homepage - view and search products"""
    query = request.GET.get('q', '')
    if query:
        products = ProductService.search_products(query)
    else:
        products = ProductService.get_all_products()
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'products/homepage.html', context)

def product_detail(request, product_id):
    """Product detail view"""
    product = ProductService.get_product_by_id(product_id)
    if not product:
        messages.error(request, 'Product not found')
        return redirect('homepage')
    
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

@login_required
def add_to_cart_view(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, message = CartService.add_to_cart(request.user, product_id, quantity)
        
        if cart_item:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    return redirect('homepage')
