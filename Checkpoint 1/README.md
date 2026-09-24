# RevoShop - Database Project (Week 1)

Proyek ini merupakan bagian dari penugasan Alternative Susulan RevoShop untuk membangun fondasi basis data relasional menggunakan PostgreSQL.

## Struktur Database (`schema.sql`)
Database `revoshop_db` terdiri dari 5 tabel utama:
1. **users**: Menyimpan data pengguna (tanpa kolom `role`).
2. **categories**: Kategori produk.
3. **products**: Data produk yang terhubung ke kategori.
4. **orders**: Data transaksi pesanan oleh pengguna.
5. **order_items**: Detail produk di dalam setiap pesanan.

## Cara Menjalankan
1. Eksekusi `schema.sql` terlebih dahulu di pgAdmin untuk membuat tabel.
2. Jalankan `seed.sql` untuk memasukkan data awal/sampel.
3. Gunakan `queries.sql` untuk melakukan pengujian kueri data.