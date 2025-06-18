# db_setup.py
#This script initializes your local SQLite database and creates required tables with two default operator logins.



import sqlite3
import os

# Create directory for product images if not exists
if not os.path.exists("assets/product_images"):
    os.makedirs("assets/product_images")

# Connect to database
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create operator table
c.execute("""
CREATE TABLE IF NOT EXISTS operator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Insert two default operators
c.execute("INSERT OR IGNORE INTO operator (username, password) VALUES ('user1', 'pass1')")
c.execute("INSERT OR IGNORE INTO operator (username, password) VALUES ('user2', 'pass2')")

# Create product master table
c.execute("""
CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    sku TEXT,
    category TEXT,
    subcategory TEXT,
    image_path TEXT,
    name TEXT,
    description TEXT,
    tax REAL,
    price REAL,
    unit TEXT
)
""")

# Create goods receiving table
c.execute("""
CREATE TABLE IF NOT EXISTS goods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    supplier TEXT,
    quantity INTEGER,
    unit TEXT,
    rate REAL,
    total REAL,
    tax REAL,
    FOREIGN KEY(product_id) REFERENCES product(id)
)
""")

# Create sales table
c.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    customer TEXT,
    quantity INTEGER,
    unit TEXT,
    rate REAL,
    total REAL,
    tax REAL,
    FOREIGN KEY(product_id) REFERENCES product(id)
)
""")

conn.commit()
conn.close()

print("Database initialized successfully.")
