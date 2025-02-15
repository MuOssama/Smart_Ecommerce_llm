import sqlite3

conn = sqlite3.connect('ecommerce.db')
c = conn.cursor()

# Create products table
c.execute('''
    CREATE TABLE IF NOT EXISTS products
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     price REAL NOT NULL,
     description TEXT)
''')

# Add sample products
sample_products = [
    ('Laptop', 999.99, 'High-performance laptop with 16GB RAM'),
    ('Smartphone', 699.99, 'Latest model with 5G capability'),
    ('Headphones', 199.99, 'Noise-cancelling wireless headphones')
]

c.executemany('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', sample_products)
conn.commit()
conn.close()