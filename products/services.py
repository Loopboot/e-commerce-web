from django.db.models import Q
from .models import Product

class ProductService:
    @staticmethod
    def get_all_products(is_active=True):
        """Get all active products"""
        return Product.objects.filter(is_active=is_active)

    @staticmethod
    def get_product_by_id(product_id):
        """Get product by ID"""
        try:
            return Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def search_products(query):
        """Search products by name, description, or category"""
        if not query:
            return Product.objects.filter(is_active=True)
        
        return Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__icontains=query),
            is_active=True
        )

    @staticmethod
    def create_product(name, description, price, stock, category, image=None):
        """Create a new product"""
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image=image
        )
        return product

    @staticmethod
    def update_product(product_id, **kwargs):
        """Update product details"""
        try:
            product = Product.objects.get(id=product_id)
            for key, value in kwargs.items():
                setattr(product, key, value)
            product.save()
            return product
        except Product.DoesNotExist:
            return None

    @staticmethod
    def delete_product(product_id):
        """Soft delete product (set is_active to False)"""
        try:
            product = Product.objects.get(id=product_id)
            product.is_active = False
            product.save()
            return True
        except Product.DoesNotExist:
            return False

    @staticmethod
    def check_stock(product_id, quantity):
        """Check if product has sufficient stock"""
        try:
            product = Product.objects.get(id=product_id)
            return product.stock >= quantity
        except Product.DoesNotExist:
            return False

    @staticmethod
    def reduce_stock(product_id, quantity):
        """Reduce product stock"""
        try:
            product = Product.objects.get(id=product_id)
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
                return True
            return False
        except Product.DoesNotExist:
            return False
