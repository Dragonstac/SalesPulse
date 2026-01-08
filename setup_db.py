import os
import random
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

def create_database():
    """Connects to default 'postgres' db to create 'salespulse_db' if missing."""
    url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
    engine = create_engine(url, isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        try:
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'"))
            if not result.fetchone():
                print(f"⚙️ Database '{DB_NAME}' not found. Creating it...")
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print(f"✅ Database '{DB_NAME}' created successfully.")
            else:
                print(f"ℹ️ Database '{DB_NAME}' already exists.")
        except Exception as e:
            print(f"❌ Error creating database: {e}")

def get_engine():
    url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def init_db():
    create_database()
    engine = get_engine()
    
    schema_sql = """
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS regions;

    CREATE TABLE regions (region_id SERIAL PRIMARY KEY, region_name VARCHAR(50));
    CREATE TABLE customers (customer_id SERIAL PRIMARY KEY, name VARCHAR(100), region_id INT REFERENCES regions(region_id), join_date DATE);
    CREATE TABLE products (product_id SERIAL PRIMARY KEY, product_name VARCHAR(100), category VARCHAR(50), price DECIMAL(10,2));
    CREATE TABLE orders (order_id SERIAL PRIMARY KEY, customer_id INT REFERENCES customers(customer_id), order_date DATE, total_amount DECIMAL(10,2));
    CREATE TABLE order_items (item_id SERIAL PRIMARY KEY, order_id INT REFERENCES orders(order_id), product_id INT REFERENCES products(product_id), quantity INT, unit_price DECIMAL(10,2));
    """
    
    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()
    print("✅ Schema Created successfully.")

    regions = ['North', 'South', 'East', 'West']
    pd.DataFrame({'region_name': regions}).to_sql('regions', engine, if_exists='append', index=False)

    products = [
        ('Enterprise Laptop', 'Electronics', 1200), ('Ergonomic Chair', 'Furniture', 300),
        ('Wireless Mouse', 'Electronics', 25), ('Standing Desk', 'Furniture', 500),
        ('Monitor 4K', 'Electronics', 400), ('Coffee Mug', 'Accessories', 15)
    ]
    pd.DataFrame(products, columns=['product_name', 'category', 'price']).to_sql('products', engine, if_exists='append', index=False)

    print("⏳ Generating 200 mock orders...")
    with engine.connect() as conn:
        r_ids = [r[0] for r in conn.execute(text("SELECT region_id FROM regions")).fetchall()]
        p_ids = conn.execute(text("SELECT product_id, price FROM products")).fetchall()
        

        for i in range(50):
            conn.execute(text(f"INSERT INTO customers (name, region_id, join_date) VALUES ('Customer {i}', {random.choice(r_ids)}, '2023-01-01')"))
        conn.commit()
        

        c_ids = [c[0] for c in conn.execute(text("SELECT customer_id FROM customers")).fetchall()]
        
        for _ in range(200):
            cust = random.choice(c_ids)
            date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
            result = conn.execute(text(f"INSERT INTO orders (customer_id, order_date, total_amount) VALUES ({cust}, '{date}', 0) RETURNING order_id"))
            order_id = result.fetchone()[0]
            
            total = 0
            for _ in range(random.randint(1, 3)):
                prod = random.choice(p_ids)
                qty = random.randint(1, 5)
                price = prod[1]
                total += (price * qty)
                conn.execute(text(f"INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES ({order_id}, {prod[0]}, {qty}, {price})"))
            
            conn.execute(text(f"UPDATE orders SET total_amount = {total} WHERE order_id = {order_id}"))
        conn.commit()
    
    print("✅ Database Seeded Complete.")

if __name__ == "__main__":
    init_db()