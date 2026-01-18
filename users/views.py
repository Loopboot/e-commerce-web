from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .services import CartService, OrderService, UserProfileService
from .models import UserProfile

@login_required
def user_profile(request):
    """User profile view"""
    profile = UserProfileService.get_or_create_profile(request.user)
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        UserProfileService.update_profile(
            request.user,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )
        messages.success(request, 'Profile updated successfully')
        return redirect('user_profile')
    
    context = {'profile': profile}
    return render(request, 'users/profile.html', context)

@login_required
def cart_view(request):
    """User cart view"""
    cart_items = CartService.get_user_cart(request.user)
    total = CartService.get_cart_total(request.user)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'users/cart.html', context)

@login_required
def update_cart(request, product_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        success, message = CartService.update_cart_item(request.user, product_id, quantity)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    """Remove item from cart"""
    success, message = CartService.remove_from_cart(request.user, product_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('cart')

@login_required
def checkout(request):
    """Checkout and create order"""
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        
        if not shipping_address:
            messages.error(request, 'Please provide shipping address')
            return redirect('cart')
        
        order, message = OrderService.create_order_from_cart(request.user, shipping_address)
        
        if order:
            messages.success(request, message)
            return redirect('order_detail', order_id=order.id)
        else:
            messages.error(request, message)
            return redirect('cart')
    
    cart_items = CartService.get_user_cart(request.user)
    total = CartService.get_cart_total(request.user)
    profile = UserProfileService.get_or_create_profile(request.user)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'profile': profile
    }
    return render(request, 'users/checkout.html', context)

@login_required
def ongoing_orders(request):
    """View ongoing orders"""
    orders = OrderService.get_ongoing_orders(request.user)
    context = {'orders': orders}
    return render(request, 'users/ongoing_orders.html', context)

@login_required
def order_history(request):
    """View order history"""
    orders = OrderService.get_order_history(request.user)
    context = {'orders': orders}
    return render(request, 'users/order_history.html', context)

@login_required
def order_detail(request, order_id):
    """View order details"""
    order = OrderService.get_order_by_id(order_id, request.user)
    
    if not order:
        messages.error(request, 'Order not found')
        return redirect('ongoing_orders')
    
    context = {'order': order}
    return render(request, 'users/order_detail.html', context)

@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    if request.method == 'POST':
        success, message = OrderService.cancel_order(order_id, request.user)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    return redirect('order_detail', order_id=order_id)

def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('homepage')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'users/register.html', context)

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('homepage')
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'users/login.html', context)

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('homepage')
