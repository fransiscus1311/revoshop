import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Impor db langsung dari models agar konteks aplikasinya menyatu
from models import db

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inisialisasi db dan migrate dengan app
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return jsonify({"message": "Selamat datang di API RevoShop - Checkpoint 3 Berhasil Terhubung!"})


@app.route('/users', methods=['POST'])
def register_user():
    from models import User
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Username, email, dan password wajib diisi!"}), 400
        
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email sudah terdaftar!"}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "Pengguna berhasil didaftarkan!",
        "user": {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    }), 201


@app.route('/auth/login', methods=['POST'])
def login_user():
    from models import User
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email dan password wajib diisi!"}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({
            "message": "Login berhasil!",
            "user_id": user.id,
            "username": user.username
        }), 200
        
    return jsonify({"error": "Email atau password salah!"}), 401


@app.route('/categories', methods=['POST'])
def create_category():
    from models import Category
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Nama kategori wajib diisi!"}), 400
        
    existing_category = Category.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({"error": "Kategori sudah ada!"}), 400
        
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({
        "message": "Kategori berhasil dibuat!",
        "category": {"id": new_category.id, "name": new_category.name}
    }), 201


@app.route('/categories', methods=['GET'])
def get_categories():
    from models import Category
    categories = Category.query.all()
    result = [{"id": cat.id, "name": cat.name} for cat in categories]
    return jsonify(result), 200


@app.route('/categories/<int:id>', methods=['GET'])
def get_category_by_id(id):
    from models import Category
    category = Category.query.get_or_404(id)
    products = [{"id": p.id, "name": p.name, "price": str(p.price)} for p in category.products] if hasattr(category, 'products') else []
    
    return jsonify({
        "id": category.id,
        "name": category.name,
        "products": products
    }), 200


@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    from models import Category
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({"error": "Nama kategori baru wajib diisi!"}), 400
        
    category.name = data['name']
    db.session.commit()
    
    return jsonify({
        "message": "Kategori berhasil diperbarui!",
        "category": {"id": category.id, "name": category.name}
    }), 200


@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    from models import Category
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({"message": "Kategori berhasil dihapus!"}), 200


@app.route('/products', methods=['POST'])
def create_product():
    from models import Category, Product
    data = request.get_json()
    if not data or not data.get('name') or not data.get('price') or not data.get('category_id'):
        return jsonify({"error": "Nama, harga, dan category_id wajib diisi!"}), 400
        
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({"error": "Kategori tidak ditemukan!"}), 404
        
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0),
        category_id=data['category_id']
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({
        "message": "Produk berhasil dibuat!",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "price": str(new_product.price),
            "stock": new_product.stock,
            "category_id": new_product.category_id
        }
    }), 201


@app.route('/products', methods=['GET'])
def get_products():
    from models import Product
    products = Product.query.all()
    result = [{
        "id": p.id,
        "name": p.name,
        "price": str(p.price),
        "stock": p.stock,
        "category_id": p.category_id
    } for p in products]
    return jsonify(result), 200


@app.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    from models import Product
    product = Product.query.get_or_404(id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock,
        "category_id": product.category_id
    }), 200


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    from models import Product
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Data pembaruan tidak boleh kosong!"}), 400
        
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.category_id = data.get('category_id', product.category_id)
    
    db.session.commit()
    
    return jsonify({
        "message": "Produk berhasil diperbarui!",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": str(product.price),
            "stock": product.stock,
            "category_id": product.category_id
        }
    }), 200


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    from models import Product
    product = Product.query.get_or_404(id)
    
    if hasattr(product, 'order_items') and product.order_items:
        return jsonify({"error": "Produk tidak dapat dihapus karena terdapat pesanan aktif yang terhubung!"}), 400
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": "Produk berhasil dihapus!"}), 200


@app.route('/orders', methods=['POST'])
def create_order():
    from models import User, Product, Order
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('items'):
        return jsonify({"error": "user_id dan items wajib diisi!"}), 400
        
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "Pengguna tidak ditemukan!"}), 404
        
    new_order = Order(user_id=data['user_id'])
    db.session.add(new_order)
    db.session.flush()
    
    total_price = 0
    order_items_list = []
    
    for item_data in data['items']:
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity', 1)
        
        product = Product.query.get(product_id)
        if not product:
            db.session.rollback()
            return jsonify({"error": f"Produk dengan ID {product_id} tidak ditemukan!"}), 404
            
        if product.stock < quantity:
            db.session.rollback()
            return jsonify({"error": f"Stok tidak cukup untuk produk: {product.name}"}), 400
            
        product.stock -= quantity
        new_order.products.append(product)
        total_price += float(product.price) * quantity
        
        order_items_list.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity,
            "price": str(product.price)
        })

    db.session.commit()
    
    return jsonify({
        "message": "Pesanan berhasil dibuat!",
        "order": {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "total_price": total_price,
            "items": order_items_list
        }
    }), 201


@app.route('/orders', methods=['GET'])
def get_orders():
    from models import Order
    orders = Order.query.all()
    result = []
    for order in orders:
        items = [{
            "id": p.id,
            "name": p.name,
            "price": str(p.price)
        } for p in order.products] if hasattr(order, 'products') else []
        
        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "items": items
        })
    return jsonify(result), 200


@app.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    from models import Order
    order = Order.query.get_or_404(id)
    items = [{
        "id": p.id,
        "name": p.name,
        "price": str(p.price)
    } for p in order.products] if hasattr(order, 'products') else []
    
    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "items": items
    }), 200


@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    from models import User, Order
    order = Order.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Data pembaruan tidak boleh kosong!"}), 400
        
    if 'user_id' in data:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "Pengguna baru tidak ditemukan!"}), 404
        order.user_id = data['user_id']
        
    db.session.commit()
    
    return jsonify({
        "message": "Pesanan berhasil diperbarui!",
        "order": {
            "id": order.id,
            "user_id": order.user_id
        }
    }), 200


@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    from models import Order
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({"message": "Pesanan berhasil dihapus!"}), 200


if __name__ == '__main__':
    app.run(debug=True)