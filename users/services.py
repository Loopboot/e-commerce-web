from django.db import transaction
from .models import Cart, Order, OrderItem, UserProfile
from products.services import ProductService

class CartService:
    @staticmethod
    def get_user_cart(user):
        """Get all cart items for a user"""
        return Cart.objects.filter(user=user).select_related('product')

    @staticmethod
    def add_to_cart(user, product_id, quantity=1):
        """Add product to cart or update quantity"""
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return None, "Product not found"

        if not ProductService.check_stock(product_id, quantity):
            return None, "Insufficient stock"

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if not ProductService.check_stock(product_id, cart_item.quantity):
                return None, "Insufficient stock"
            cart_item.save()

        return cart_item, "Added to cart"

    @staticmethod
    def update_cart_item(user, product_id, quantity):
        """Update cart item quantity"""
        try:
            cart_item = Cart.objects.get(user=user, product_id=product_id)
            if quantity <= 0:
                cart_item.delete()
                return True, "Item removed from cart"
            
            if not ProductService.check_stock(product_id, quantity):
                return False, "Insufficient stock"
            
            cart_item.quantity = quantity
            cart_item.save()
            return True, "Cart updated"
        except Cart.DoesNotExist:
            return False, "Item not found in cart"

    @staticmethod
    def remove_from_cart(user, product_id):
        """Remove item from cart"""
        try:
            cart_item = Cart.objects.get(user=user, product_id=product_id)
            cart_item.delete()
            return True, "Item removed from cart"
        except Cart.DoesNotExist:
            return False, "Item not found in cart"

    @staticmethod
    def clear_cart(user):
        """Clear all items from user's cart"""
        Cart.objects.filter(user=user).delete()

    @staticmethod
    def get_cart_total(user):
        """Calculate total cart value"""
        cart_items = Cart.objects.filter(user=user).select_related('product')
        total = sum(item.get_total_price() for item in cart_items)
        return total


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user, shipping_address):
        """Create order from user's cart"""
        cart_items = Cart.objects.filter(user=user).select_related('product')
        
        if not cart_items.exists():
            return None, "Cart is empty"

        # Calculate total
        total_amount = sum(item.get_total_price() for item in cart_items)

        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            shipping_address=shipping_address
        )

        # Create order items and reduce stock
        for cart_item in cart_items:
            if not ProductService.check_stock(cart_item.product.id, cart_item.quantity):
                transaction.set_rollback(True)
                return None, f"Insufficient stock for {cart_item.product.name}"

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

            ProductService.reduce_stock(cart_item.product.id, cart_item.quantity)

        # Clear cart
        CartService.clear_cart(user)

        return order, "Order placed successfully"

    @staticmethod
    def get_user_orders(user):
        """Get all orders for a user"""
        return Order.objects.filter(user=user).prefetch_related('items__product')

    @staticmethod
    def get_ongoing_orders(user):
        """Get ongoing orders (not delivered or cancelled)"""
        return Order.objects.filter(
            user=user,
            status__in=['pending', 'processing', 'shipped']
        ).prefetch_related('items__product')

    @staticmethod
    def get_order_history(user):
        """Get completed orders"""
        return Order.objects.filter(
            user=user,
            status__in=['delivered', 'cancelled']
        ).prefetch_related('items__product')

    @staticmethod
    def get_order_by_id(order_id, user=None):
        """Get order by ID"""
        try:
            if user:
                return Order.objects.get(id=order_id, user=user)
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id, user):
        """Cancel an order and restore stock"""
        order = OrderService.get_order_by_id(order_id, user)
        
        if not order:
            return False, "Order not found"

        if order.status in ['delivered', 'cancelled']:
            return False, f"Cannot cancel {order.status} order"

        # Restore stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = 'cancelled'
        order.save()

        return True, "Order cancelled successfully"

    @staticmethod
    def update_order_status(order_id, status):
        """Update order status (admin function)"""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            return False, "Order not found"

        order.status = status
        order.save()
        return True, "Order status updated"


class UserProfileService:
    @staticmethod
    def get_or_create_profile(user):
        """Get or create user profile"""
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def update_profile(user, **kwargs):
        """Update user profile"""
        profile = UserProfileService.get_or_create_profile(user)
        for key, value in kwargs.items():
            setattr(profile, key, value)
        profile.save()
        return profile
