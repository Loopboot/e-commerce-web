from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import Product
from products.services import ProductService
from users.models import Order
from users.services import OrderService

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard"""
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'pending_orders': pending_orders
    }
    return render(request, 'shop_admin/dashboard.html', context)

@staff_member_required
def manage_products(request):
    """Manage products"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop_admin/manage_products.html', context)

@staff_member_required
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = float(request.POST.get('price'))
        stock = int(request.POST.get('stock'))
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        ProductService.create_product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image=image
        )
        messages.success(request, 'Product added successfully')
        return redirect('manage_products')
    
    return render(request, 'shop_admin/add_product.html')

@staff_member_required
def edit_product(request, product_id):
    """Edit product"""
    product = ProductService.get_product_by_id(product_id)
    
    if not product:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            messages.error(request, 'Product not found')
            return redirect('manage_products')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = float(request.POST.get('price'))
        stock = int(request.POST.get('stock'))
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        update_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock': stock,
            'category': category
        }
        
        if image:
            update_data['image'] = image
        
        ProductService.update_product(product_id, **update_data)
        messages.success(request, 'Product updated successfully')
        return redirect('manage_products')
    
    context = {'product': product}
    return render(request, 'shop_admin/edit_product.html', context)

@staff_member_required
def delete_product(request, product_id):
    """Delete product"""
    if request.method == 'POST':
        ProductService.delete_product(product_id)
        messages.success(request, 'Product deleted successfully')
    
    return redirect('manage_products')

@staff_member_required
def manage_orders(request):
    """Manage orders"""
    orders = Order.objects.all().select_related('user')
    context = {'orders': orders}
    return render(request, 'shop_admin/manage_orders.html', context)

@staff_member_required
def update_order_status_view(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        status = request.POST.get('status')
        success, message = OrderService.update_order_status(order_id, status)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    return redirect('manage_orders')

@staff_member_required
def manage_users(request):
    """Manage users"""
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'shop_admin/manage_users.html', context)
