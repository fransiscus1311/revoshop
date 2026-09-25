from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def create_order(self):
        """Mensimulasikan pembuatan pesanan baru (POST /orders)"""
        payload = {
            "user_id": 1,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 1
                }
            ]
        }
        response = self.client.post("/orders", json=payload)
        if response.status_code >= 400:
            print(f"Error {response.status_code}: {response.text}")

    @task(2)
    def view_orders(self):
        """Mensimulasikan pengambilan daftar pesanan pengguna"""
        self.client.get("/orders")

    @task(2)
    def view_products(self):
        """Mensimulasikan melihat daftar produk"""
        self.client.get("/products")

    @task(1)
    def view_single_product(self):
        """Mensimulasikan melihat detail produk ID 1"""
        self.client.get("/products/1")