# 🐍 Django E-Commerce Platform

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Made with ❤️ by Kaiser-iDusk](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)]()

### Description

A modern, user-friendly e-commerce platform built with Django, featuring secure user authentication, product management, cart functionality, and a streamlined checkout process.

### 📋 Summary

This project is a full-featured e-commerce web application built using Django, designed for seamless online shopping. It supports user registration with two-factor authentication (2FA), product browsing, cart management, secure checkout with address and delivery time selection, and order tracking. The platform ensures a robust user experience with Tailwind CSS styling and includes features like out-of-stock handling, order confirmation emails, and return requests.

### Key Features

- <b>User Authentication </b>: Secure login/registration with 2FA (console-based OTP).

- <b>Product Management </b>: Browse products, view details, and manage stock.

- <b>Cart </b>: Add/remove items, update quantities, and calculate totals dynamically.

- <b>Checkout </b>: Select or add addresses, choose delivery time (with 1-minute buffer validation), and proceed to payment.

- <b>Order Processing </b>: Orders remain in "confirmed" state until marked "delivered," with console-based email notifications.

- <b>Search & Recommendations </b>: Search products and view recommendations for out-of-stock items.

- <b>Returns </b>: Request returns for completed orders.

### Tech Stack

- <b>Backend </b>: Django 4.x, Python 3.x

- <b>Frontend </b>: Tailwind CSS for responsive styling

- <b>Database </b>: SQLite (development), PostgreSQL (production)

- <b>Authentication </b>: Django Authentication with custom EmailBackend, phonenumber_field for 2FA

- <b>Email </b>: Console-based email backend (configurable for SMTP in production)

- <b>Other </b>: requests for API calls (product population), uuid for unique order IDs

### 🚀 Setup and Usage

Follow these steps to set up and run the project locally.

<b>Prerequisites: </b>

- Python 3.8+
- Virtualenv
- Git
- (Optional) PostgreSQL for production database

### Installation

Follow the steps below for installation:

- Clone the Repository:

```bash
git clone <repository-url>
cd e-com
```

- Set Up Virtual Environment:

```bash
python -m venv myenv
.\myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

- Install Dependencies:

```bash
pip install -r requirements.txt
```

Note: If requirements.txt is missing, install:

```bash
pip install django requests python-decouple phonenumber_field
```

- Configure Environment Variables: Create a .env file in D:\Python\files\e-com:

```
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

Note: Generate a SECRET_KEY using a secure random string generator.

- Apply Migrations:

```python
python manage.py makemigrations
python manage.py migrate
```

- Populate Products: Seed the database with sample products:

```python
python manage.py populate_products
```

- Create Superuser (for admin access):

```python
python manage.py createsuperuser
```

- Run the Development Server:

```python
python manage.py runserver
```

Access the app at http://127.0.0.1:8000.

### Usage

<b> Register/Login: </b>
- Visit http://127.0.0.1:8000/accounts/register/ to create an account.
- Log in at http://127.0.0.1:8000/accounts/login/ with 2FA (check terminal for OTP).

<b> Browse for Products: </b>
- View products at http://127.0.0.1:8000/.
- Use the search bar to find specific items.

<b> Manage Cart based on session: </b>
- Add products to cart via http://127.0.0.1:8000/add_to_cart/<product_id>/.
- View and update cart at http://127.0.0.1:8000/cart/.

<b> Checkout: </b>
-Proceed to checkout from the cart.
- Select an existing address or add a new one.
- Choose a delivery time (must be at least 1 minute in the future).
- Proceed to payment and select a payment method.

<b> Order Management: </b>
- View order history at http://127.0.0.1:8000/accounts/profile/.
- Submit return requests for delivered orders.
- Mark orders as delivered (admin or via http://127.0.0.1:8000/mark_delivered/<order_id>/).

<b> Admin Panel: </b>
- Access at http://127.0.0.1:8000/admin/ to manage products, orders, and users.

### 📷 Screenshots

Note: Replace <image-path> with actual paths to screenshots once captured.





Homepage
Displays product listings with search functionality.
![Homepage](/homepage.png)



Cart Page
Shows cart items with quantity controls and total calculation.
![Cart](/cart.png)



Checkout Page
Address selection and delivery time picker with validation.
![Checkout](/checkout.png)



Payment Page
Payment method selection for order completion.
![Payment](/payment.png)



Order Confirmation
Confirmation screen after successful order placement.
![Order Confirmation](/order_confirmation.png)



🛠️ Development Notes





Custom Template Tags: The multiply filter (shop/templatetags/shop_tags.py) calculates cart item totals.



2FA: Console-based OTP for development; configure Twilio for production.



Emails: Console-based in development (EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'); configure SMTP for production.



Stock Management: Products are removed when stock reaches zero; no restocking on returns.



Celery: Removed due to Windows compatibility issues; synchronous tasks used for emails.

🐛 Troubleshooting





Template Errors: Ensure shop/templatetags/shop_tags.py and __init__.py exist, and restart the server.



Form Validation: Check terminal for form errors if checkout fails.



Database Issues: Run python manage.py makemigrations and migrate after model changes.



Logs: Check terminal or DEBUG=True logs for errors.

For issues, check the Django admin or share error tracebacks.

📬 Contact

For support or contributions, contact [your-email@example.com] or open an issue on the repository.