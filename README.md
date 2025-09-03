# 🛒 PhiMart - E-commerce API

PhiMart is a fully-featured e-commerce backend built using Django and Django REST Framework (DRF). It includes essential functionality like authentication, product management, cart and order processing, and admin dashboards.

---

## 🚀 Features

- 🔐 JWT Authentication (Register, Login, Logout, Token Refresh)
- 🧾 Product & Category Management (CRUD)
- 🛍️ Shopping Cart System
- 📦 Order Placement & Status Updates
- 👤 User Profile Management
- 📊 Admin Dashboard with Metrics

---

## 📁 Project Structure

```
phimart/
├── auth/             # Authentication logic (JWT)
├── products/         # Product and category logic
├── cart/             # Shopping cart management
├── orders/           # Order and order items
├── users/            # User profiles
├── dashboard/        # Admin-specific endpoints
└── ...
```

---

## 🔐 Authentication Endpoints

| Method | Endpoint                  | Description               |
|--------|---------------------------|---------------------------|
| POST   | `/auth/register/`         | Register a new user       |
| POST   | `/auth/login/`            | Login & receive token     |
| POST   | `/auth/logout/`           | Logout the user           |
| POST   | `/auth/token/refresh/`    | Refresh JWT token         |

---

## 📚 Category Endpoints

| Method | Endpoint                  | Description                  |
|--------|---------------------------|------------------------------|
| GET    | `/api/categories/`        | List all categories          |
| GET    | `/api/categories/<id>/`   | Get a specific category      |
| POST   | `/api/categories/`        | Create a new category (admin)|
| PUT    | `/api/categories/<id>/`   | Update a category            |
| DELETE | `/api/categories/<id>/`   | Delete a category            |

---

## 📦 Product Endpoints

| Method | Endpoint                            | Description                       |
|--------|-------------------------------------|-----------------------------------|
| GET    | `/api/products/`                    | List all products                 |
| GET    | `/api/products/<id>/`               | Get a specific product            |
| GET    | `/api/products/?search=query`       | Search by name/description        |
| GET    | `/api/products/?category=id`        | Filter by category                |
| POST   | `/api/products/`                    | Create new product (admin)        |
| PUT    | `/api/products/<id>/`               | Update a product (admin)          |
| DELETE | `/api/products/<id>/`               | Delete a product (admin)          |

---

## 🛒 Cart Endpoints

| Method | Endpoint                                       | Description              |
|--------|------------------------------------------------|--------------------------|
| POST   | `/api/carts/`                                  | Create a new cart        |
| GET    | `/api/carts/<cart_id>/`                        | Retrieve a cart          |
| DELETE | `/api/carts/<cart_id>/`                        | Delete a cart            |
| POST   | `/api/carts/<cart_id>/items/`                  | Add item to cart         |
| PATCH  | `/api/carts/<cart_id>/items/<item_id>/`        | Update quantity          |
| DELETE | `/api/carts/<cart_id>/items/<item_id>/`        | Remove item              |

---

## 📦 Order Endpoints

| Method | Endpoint                        | Description                     |
|--------|----------------------------------|---------------------------------|
| GET    | `/api/orders/`                  | List all orders (user)         |
| GET    | `/api/orders/<id>/`             | Get specific order             |
| POST   | `/api/orders/`                  | Place new order                |
| PUT    | `/api/orders/<id>/status/`      | Update order status (admin)    |
| DELETE | `/api/orders/<id>/`             | Cancel order                   |

---

## 👤 User Profile Endpoints

| Method | Endpoint         | Description                |
|--------|------------------|----------------------------|
| GET    | `/api/profile/`  | Get user profile           |
| PUT    | `/api/profile/`  | Update user profile        |

---

## 📊 Admin Dashboard Endpoints

| Method | Endpoint                          | Description                      |
|--------|-----------------------------------|----------------------------------|
| GET    | `/api/dashboard/total-users/`     | Total registered users           |
| GET    | `/api/dashboard/total-orders/`    | Total number of orders           |
| GET    | `/api/dashboard/total-products/`  | Total available products         |

---

## 🧱 Models Overview

- **User**: `first_name`, `last_name`, `email`, `phone_number`, `address`, `password`
- **Category**: `name`, `description`
- **Product**: `name`, `description`, `price`, `stock`, `category`, `image`
- **Cart**: One-to-One with User
- **CartItem**: FK to Cart and Product
- **Order**: FK to User, `status`, `total_price`
- **OrderItem**: FK to Order and Product

---

## 🛠 Setup & Run (Local)

```bash
# Clone the repo
git clone https://github.com/your-username/phimart-backend.git
cd phimart-backend

# Setup virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

---
## Doccumentation

[![Swagger Docs](https://img.shields.io/badge/API-Swagger-blue)](https://pi-commerce-ten.vercel.app/docs)


## ✅ Future Enhancements

- Payment gateway integration
- Inventory alerts

---

## 🧑‍💻 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
