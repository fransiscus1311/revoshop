from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Konfigurasi database PostgreSQL lokal (sesuaikan password jika berbeda)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin2701@localhost/revoshop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Category, Product, Order, order_items

@app.route('/')
def home():
    return jsonify({"message": "Selamat datang di API RevoShop - Checkpoint 2 Berhasil Terhubung!"})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "category_id": p.category_id
        })
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Produk tidak ditemukan"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "category_id": product.category_id
    })

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({"error": "Username dan email wajib diisi"}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email sudah digunakan"}), 400
        
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data.get('password_hash', 'default_hashed_pass')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User berhasil didaftarkan",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    })

if __name__ == '__main__':
    app.run(debug=True)