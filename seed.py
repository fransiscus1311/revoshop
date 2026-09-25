from app import app, db
from models import Category, Product, User

with app.app_context():
    # Buat kategori jika belum ada
    if not Category.query.first():
        category = Category(name="Elektronik")
        db.session.add(category)
        db.session.commit()
    
    # Cek produk ID 1, update stoknya secara paksa menjadi 10000
    product = Product.query.get(1)
    if product:
        product.stock = 10000
    else:
        product = Product(
            id=1,
            name="Laptop Gaming",
            price=15000000,
            stock=10000,
            category_id=1
        )
        db.session.add(product)
    db.session.commit()
    
    # Buat user ID 1 jika belum ada
    if not User.query.get(1):
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password_hash="dummy_hash_password"
        )
        db.session.add(user)
        db.session.commit()

    print("Stok produk berhasil diperbarui menjadi 10.000!")