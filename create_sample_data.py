#!/usr/bin/env python
"""
Script to create sample data for testing the e-commerce website
Run: python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from products.models import Product
from users.models import UserProfile

# Create superuser
print("Creating superuser...")
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print(f"Superuser created: username=admin, password=admin123")
else:
    print("Superuser already exists")

# Create test users
print("\nCreating test users...")
test_users = [
    ('john', 'john@example.com', 'john123'),
    ('jane', 'jane@example.com', 'jane123'),
]

for username, email, password in test_users:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, email, password)
        UserProfile.objects.create(
            user=user,
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            state='Test State',
            pincode='12345'
        )
        print(f"User created: username={username}, password={password}")
    else:
        print(f"User {username} already exists")

# Create sample products
print("\nCreating sample products...")
sample_products = [
    {
        'name': 'Laptop',
        'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
        'price': 999.99,
        'stock': 10,
        'category': 'Electronics'
    },
    {
        'name': 'Smartphone',
        'description': 'Latest smartphone with 5G connectivity and 128GB storage',
        'price': 699.99,
        'stock': 20,
        'category': 'Electronics'
    },
    {
        'name': 'Wireless Headphones',
        'description': 'Noise-cancelling wireless headphones with 30-hour battery life',
        'price': 199.99,
        'stock': 30,
        'category': 'Electronics'
    },
    {
        'name': 'Smart Watch',
        'description': 'Fitness tracking smartwatch with heart rate monitor',
        'price': 299.99,
        'stock': 15,
        'category': 'Electronics'
    },
    {
        'name': 'Tablet',
        'description': '10-inch tablet with stylus support and 256GB storage',
        'price': 499.99,
        'stock': 12,
        'category': 'Electronics'
    },
    {
        'name': 'Bluetooth Speaker',
        'description': 'Portable Bluetooth speaker with waterproof design',
        'price': 79.99,
        'stock': 25,
        'category': 'Electronics'
    },
    {
        'name': 'USB-C Cable',
        'description': 'High-speed USB-C charging cable 2 meters',
        'price': 19.99,
        'stock': 50,
        'category': 'Accessories'
    },
    {
        'name': 'Keyboard',
        'description': 'Mechanical keyboard with RGB backlighting',
        'price': 129.99,
        'stock': 18,
        'category': 'Accessories'
    },
    {
        'name': 'Mouse',
        'description': 'Ergonomic wireless mouse with precision tracking',
        'price': 49.99,
        'stock': 35,
        'category': 'Accessories'
    },
    {
        'name': 'Monitor',
        'description': '27-inch 4K monitor with HDR support',
        'price': 449.99,
        'stock': 8,
        'category': 'Electronics'
    },
]

for product_data in sample_products:
    if not Product.objects.filter(name=product_data['name']).exists():
        Product.objects.create(**product_data)
        print(f"Product created: {product_data['name']}")
    else:
        print(f"Product {product_data['name']} already exists")

print("\n=== Sample Data Creation Complete ===")
print("\nLogin credentials:")
print("Admin: username=admin, password=admin123")
print("Test User 1: username=john, password=john123")
print("Test User 2: username=jane, password=jane123")
print("\nRun the server with: python manage.py runserver")
