import pytest
from app import app, db
from models import Category, Product

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_home_route(client):
    """Menguji rute utama API"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "Selamat datang di API RevoShop" in data["message"]

def test_get_products_empty(client):
    """Menguji rute GET /products saat data produk kosong"""
    response = client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_and_get_category(client):
    """Menguji pembuatan dan pengambilan data kategori"""
    # Buat kategori baru
    response = client.post('/categories', json={"name": "Elektronik"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["category"]["name"] == "Elektronik"
    
    # Ambil daftar kategori
    res_get = client.get('/categories')
    assert res_get.status_code == 200
    categories = res_get.get_json()
    assert len(categories) == 1
    assert categories[0]["name"] == "Elektronik"