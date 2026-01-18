# E-Commerce Website

A fully functional e-commerce website built with Django, featuring a modular architecture with separate service layers, models, views, and templates.

## Features

### Homepage
- View all products
- Search products by name, description, or category
- Add products to cart
- View product details

### User Features
- User registration and authentication
- User profile management
- Shopping cart functionality
- Checkout and order placement
- View ongoing orders
- View order history
- Cancel orders (for pending/processing orders)

### Admin Features (Staff Only)
- Admin dashboard with statistics
- Manage products (Add, Edit, Delete)
- Manage orders and update order status
- View all users

## Architecture

### Modular Structure
```
e-commerce-web/
├── products/           # Product management app
│   ├── models.py      # Product model
│   ├── services.py    # Business logic layer
│   ├── views.py       # View controllers
│   ├── urls.py        # URL routing
│   └── templates/     # Product templates
├── users/             # User management app
│   ├── models.py      # User, Cart, Order models
│   ├── services.py    # Business logic layer
│   ├── views.py       # View controllers
│   ├── urls.py        # URL routing
│   └── templates/     # User templates
├── shop_admin/        # Admin management app
│   ├── views.py       # Admin views
│   ├── urls.py        # Admin URL routing
│   └── templates/     # Admin templates
├── static/            # Static files
│   ├── css/           # Separate CSS files
│   └── js/            # Separate JavaScript files
├── templates/         # Base templates
└── media/             # User-uploaded media files
```

### Service Layer
Each app includes a `services.py` file that contains the business logic:
- **ProductService**: Handles product operations (CRUD, search, stock management)
- **CartService**: Manages shopping cart operations
- **OrderService**: Handles order creation, cancellation, and status updates
- **UserProfileService**: Manages user profile information

## Installation

### Prerequisites
- Python 3.14+
- Poetry (for dependency management)

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /mnt/diskd/Projects/e-commerce-web
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Run migrations (if not already done):**
   ```bash
   poetry run python manage.py migrate
   ```

4. **Create sample data (if not already done):**
   ```bash
   poetry run python manage.py shell < create_sample_data.py
   ```

5. **Run the development server:**
   ```bash
   poetry run python manage.py runserver
   ```

6. **Access the website:**
   - Homepage: http://127.0.0.1:8000/
   - Admin Dashboard: http://127.0.0.1:8000/shop-admin/dashboard/
   - Django Admin: http://127.0.0.1:8000/django-admin/

## Default Credentials

### Admin User (Staff Access)
- Username: `admin`
- Password: `admin123`

### Test Users
- Username: `john` / Password: `john123`
- Username: `jane` / Password: `jane123`

## URL Structure

### Public URLs
- `/` - Homepage (product listing and search)
- `/product/<id>/` - Product detail page
- `/users/register/` - User registration
- `/users/login/` - User login

### User URLs (Login Required)
- `/users/profile/` - User profile
- `/users/cart/` - Shopping cart
- `/users/checkout/` - Checkout page
- `/users/orders/ongoing/` - Ongoing orders
- `/users/orders/history/` - Order history
- `/order/<id>/` - Order detail

### Admin URLs (Staff Only)
- `/shop-admin/dashboard/` - Admin dashboard
- `/shop-admin/products/` - Manage products
- `/shop-admin/products/add/` - Add new product
- `/shop-admin/products/edit/<id>/` - Edit product
- `/shop-admin/orders/` - Manage orders
- `/shop-admin/users/` - Manage users

## Models

### Product Model
- Name, description, price, stock
- Category and image
- Active/inactive status
- Timestamps

### Cart Model
- User, product, quantity
- Unique constraint per user-product pair

### Order Model
- User, items, total amount
- Status (pending, processing, shipped, delivered, cancelled)
- Shipping address
- Timestamps

### UserProfile Model
- One-to-one with Django User
- Phone, address, city, state, pincode

## Key Features Implementation

### Service Layer Pattern
All business logic is separated into service classes:
- Easier testing and maintenance
- Better separation of concerns
- Reusable across views

### Modular Templates
Each app has its own templates directory:
- `products/templates/products/` - Product views
- `users/templates/users/` - User views
- `shop_admin/templates/shop_admin/` - Admin views
- `templates/` - Base template

### Separate Static Files
- `static/css/style.css` - All CSS styles
- `static/js/main.js` - Global JavaScript
- `static/js/products.js` - Product-specific JavaScript
- `static/js/cart.js` - Cart-specific JavaScript
- `static/js/admin.js` - Admin-specific JavaScript

### Transaction Safety
Order creation uses database transactions to ensure:
- Stock is properly reduced
- Cart is cleared only on successful order
- All operations are atomic

## Technologies Used

- **Backend**: Django 6.0.1
- **Database**: SQLite3 (development)
- **Image Handling**: Pillow 12.1.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Dependency Management**: Poetry

## Development

### Adding New Products
1. Login as admin
2. Navigate to `/shop-admin/products/`
3. Click "Add New Product"
4. Fill in product details and submit

### Managing Orders
1. Login as admin
2. Navigate to `/shop-admin/orders/`
3. Update order status using dropdown
4. Status changes are saved automatically

### Testing the Checkout Flow
1. Register/login as a regular user
2. Browse products on homepage
3. Add products to cart
4. Go to cart and update quantities
5. Proceed to checkout
6. Enter shipping address
7. Place order
8. View order in "My Orders"

## Security Considerations

⚠️ **For Production Deployment:**
- Change `SECRET_KEY` in `settings.py`
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL or MySQL instead of SQLite
- Set up proper media file serving (e.g., AWS S3)
- Enable HTTPS
- Configure email backend for notifications

## Future Enhancements

- Payment gateway integration
- Email notifications
- Product reviews and ratings
- Wishlist functionality
- Advanced filtering and sorting
- Order tracking
- Invoice generation
- Multi-currency support

## License

This project is created for educational purposes.

## Support

For issues or questions, please contact the development team.
