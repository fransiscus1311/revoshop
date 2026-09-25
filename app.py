import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Impor db langsung dari models agar konteks aplikasinya menyatu
from models import db

app = Flask(__name__)

# Konfigurasi Database SQLite lokal/cloud
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///revoshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Root Endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Selamat datang di API RevoShop - Checkpoint 3 Berhasil Terhubung!"}), 200

# Endpoint Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    return jsonify({
        "message": "Registrasi berhasil!",
        "user": {
            "username": username,
            "email": email
        }
    }), 201

# Endpoint Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email == "test@email.com" and password == "password123":
        return jsonify({
            "message": "Login berhasil!",
            "token": "dummy-jwt-token-revoshop-2026"
        }), 200
    else:
        return jsonify({"error": "Email atau password salah!"}), 401

# Endpoint Daftar Produk (GET)
@app.route('/api/products', methods=['GET'])
def get_products():
    sample_products = [
        {"id": 1, "name": "Jaket Almamater BINUS", "price": 250000},
        {"id": 2, "name": "Kaos RevoShop Official", "price": 100000}
    ]
    return jsonify({
        "message": "Berhasil memuat data produk",
        "products": sample_products
    }), 200

# Endpoint Keranjang Belanja (POST)
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    return jsonify({
        "message": "Produk berhasil ditambahkan ke keranjang",
        "cart_item": {
            "product_id": product_id,
            "quantity": quantity
        }
    }), 201

# Endpoint Checkout (POST)
@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    shipping_address = data.get('address')
    
    return jsonify({
        "message": "Checkout berhasil! Pesanan sedang diproses.",
        "order_details": {
            "address": shipping_address,
            "status": "Success"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)