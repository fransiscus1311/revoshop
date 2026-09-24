-- 1. Menampilkan semua produk beserta nama kategorinya (JOIN)
SELECT p.id, p.name AS product_name, p.price, p.stock, c.name AS category_name
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;

-- 2. Menampilkan riwayat pesanan beserta nama pembelinya
SELECT o.id AS order_id, u.name AS customer_name, o.total_price, o.status, o.created_at
FROM orders o
JOIN users u ON o.user_id = u.id;

-- 3. Menampilkan detail item barang dalam suatu pesanan
OI.id AS item_id, o.id AS order_id, p.name AS product_name, oi.quantity, oi.subtotal
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id;