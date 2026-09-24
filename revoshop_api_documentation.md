# RevoShop API Documentation (Checkpoint 3)

This document provides a comprehensive overview of all API endpoints implemented in the RevoShop backend application, structured for testing and integration.

---

## Base URL
```text
http://127.0.0.1:5000
```

---

## 1. Authentication & Users

### Register User
* **URL:** `/users`
* **Method:** `POST`
* **Description:** Registers a new user with a hashed password.
* **Request Body (JSON):**
  ```json
  {
    "username": "fransiscus",
    "email": "fransiscus@example.com",
    "password": "password123"
  }
  ```
* **Success Response (`201 CREATED`):**
  ```json
  {
    "message": "Pengguna berhasil didaftarkan!",
    "user": {
      "id": 1,
      "username": "fransiscus",
      "email": "fransiscus@example.com"
    }
  }
  ```

### Login User
* **URL:** `/auth/login`
* **Method:** `POST`
* **Description:** Authenticates a registered user.
* **Request Body (JSON):**
  ```json
  {
    "email": "fransiscus@example.com",
    "password": "password123"
  }
  ```
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Login berhasil!",
    "user_id": 1,
    "username": "fransiscus"
  }
  ```

---

## 2. Categories

### Create Category
* **URL:** `/categories`
* **Method:** `POST`
* **Description:** Adds a new product category.
* **Request Body (JSON):**
  ```json
  {
    "name": "Elektronik"
  }
  ```
* **Success Response (`201 CREATED`):**
  ```json
  {
    "message": "Kategori berhasil dibuat!",
    "category": {
      "id": 1,
      "name": "Elektronik"
    }
  }
  ```

### Get All Categories
* **URL:** `/categories`
* **Method:** `GET`
* **Description:** Retrieves a list of all categories.
* **Success Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "name": "Elektronik"
    }
  ]
  ```

### Get Category by ID
* **URL:** `/categories/<id>`
* **Method:** `GET`
* **Description:** Retrieves details of a specific category along with its associated products.
* **Success Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "name": "Elektronik",
    "products": [
      {
        "id": 1,
        "name": "Laptop Gaming",
        "price": "15000000.00"
      }
    ]
  }
  ```

### Update Category
* **URL:** `/categories/<id>`
* **Method:** `PUT`
* **Description:** Updates an existing category's name.
* **Request Body (JSON):**
  ```json
  {
    "name": "Gadget & Elektronik"
  }
  ```
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Kategori berhasil diperbarui!",
    "category": {
      "id": 1,
      "name": "Gadget & Elektronik"
    }
  }
  ```

### Delete Category
* **URL:** `/categories/<id>`
* **Method:** `DELETE`
* **Description:** Deletes a category by its ID.
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Kategori berhasil dihapus!"
  }
  ```

---

## 3. Products

### Create Product
* **URL:** `/products`
* **Method:** `POST`
* **Description:** Adds a new product under a specific category.
* **Request Body (JSON):**
  ```json
  {
    "name": "Laptop Gaming",
    "price": 15000000,
    "stock": 10,
    "category_id": 1
  }
  ```
* **Success Response (`201 CREATED`):**
  ```json
  {
    "message": "Produk berhasil dibuat!",
    "product": {
      "id": 1,
      "name": "Laptop Gaming",
      "price": "15000000",
      "stock": 10,
      "category_id": 1
    }
  }
  ```

### Get All Products
* **URL:** `/products`
* **Method:** `GET`
* **Description:** Retrieves a list of all products.
* **Success Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "name": "Laptop Gaming",
      "price": "15000000.00",
      "stock": 10,
      "category_id": 1
    }
  ]
  ```

### Get Product by ID
* **URL:** `/products/<id>`
* **Method:** `GET`
* **Description:** Retrieves details of a specific product.
* **Success Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "name": "Laptop Gaming",
    "price": "15000000.00",
    "stock": 10,
    "category_id": 1
  }
  ```

### Update Product
* **URL:** `/products/<id>`
* **Method:** `PUT`
* **Description:** Updates product information (price, stock, name, or category).
* **Request Body (JSON):**
  ```json
  {
    "price": 14500000,
    "stock": 8
  }
  ```
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Produk berhasil diperbarui!",
    "product": {
      "id": 1,
      "name": "Laptop Gaming",
      "price": "14500000.00",
      "stock": 8,
      "category_id": 1
    }
  }
  ```

### Delete Product
* **URL:** `/products/<id>`
* **Method:** `DELETE`
* **Description:** Deletes a product if not tied to any active orders.
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Produk berhasil dihapus!"
  }
  ```

---

## 4. Orders

### Create Order
* **URL:** `/orders`
* **Method:** `POST`
* **Description:** Places an order, calculates total price, and deducts product stock automatically.
* **Request Body (JSON):**
  ```json
  {
    "user_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }
  ```
* **Success Response (`201 CREATED`):**
  ```json
  {
    "message": "Pesanan berhasil dibuat!",
    "order": {
      "id": 1,
      "user_id": 1,
      "total_price": 30000000.0,
      "items": [
        {
          "product_id": 1,
          "product_name": "Laptop Gaming",
          "quantity": 2,
          "price": "15000000.00"
        }
      ]
    }
  }
  ```

### Get All Orders
* **URL:** `/orders`
* **Method:** `GET`
* **Description:** Retrieves a list of all orders.
* **Success Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "name": "Laptop Gaming",
          "price": "15000000.00"
        }
      ]
    }
  ]
  ```

### Get Order by ID
* **URL:** `/orders/<id>`
* **Method:** `GET`
* **Description:** Retrieves details of a specific order.
* **Success Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "user_id": 1,
    "items": [
      {
        "id": 1,
        "name": "Laptop Gaming",
        "price": "15000000.00"
      }
    ]
  }
  ```

### Delete Order
* **URL:** `/orders/<id>`
* **Method:** `DELETE`
* **Description:** Cancels/deletes an order by its ID.
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Pesanan berhasil dihapus!"
  }
  ```