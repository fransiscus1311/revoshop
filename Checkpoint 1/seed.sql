-- 1. Insert Data Users (Tanpa kolom role)
INSERT INTO users (name, email, password) VALUES
('Budi Santoso', 'budi@example.com', 'hashed_password_123'),
('Siti Aminah', 'siti@example.com', 'hashed_password_456');

-- 2. Insert Data Categories
INSERT INTO categories (name, description) VALUES
('Elektronik', 'Perangkat elektronik dan gawai'),
('Pakaian', 'Pakaian pria dan wanita');

-- 3. Insert Data Products
INSERT INTO products (name, price, stock, category_id) VALUES
('Smartphone Android', 2500000.00, 10, 1),
('Kemeja Flanel', 150000.00, 25, 2);

-- 4. Insert Data Orders
INSERT INTO orders (user_id, total_price, status) VALUES
(1, 2650000.00, 'Completed');

-- 5. Insert Data Order Items
INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES
(1, 1, 1, 2500000.00),
(1, 2, 1, 150000.00);