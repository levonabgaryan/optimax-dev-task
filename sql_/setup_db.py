import sqlite3
from pathlib import Path
import json
from typing import Any, Final


BASE_DIR: Final[Path] = Path(__file__).resolve().parent
DB_PATH: Final[Path] = BASE_DIR / "data" / "SqlLite.db"
JSON_PATH: Final[Path] = BASE_DIR / "data" / "data.json"


def create_tables() -> None:
    # This function create a SqlLite db file, run migrations
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        connection.execute("PRAGMA foreign_keys = ON;")
        cursor.executescript(
            """
            -- Customers table
            CREATE TABLE IF NOT EXISTS customers (
                   customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name VARCHAR(50),
                   last_name VARCHAR(50),
                   email VARCHAR(100) UNIQUE,
                   phone VARCHAR(20),
                   address VARCHAR(200),
                   city VARCHAR(50),
                   country VARCHAR(50),
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   last_login_date TIMESTAMP,
                   total_orders INTEGER DEFAULT 0,
                   customer_segment VARCHAR(20)
            );
            
            -- Orders table
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20),
                shipping_method VARCHAR(50),
                shipping_address VARCHAR(200),
                shipping_city VARCHAR(50),
                shipping_country VARCHAR(50),
                total_amount DECIMAL(10,2),
                payment_method VARCHAR(50),
                payment_status VARCHAR(20),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
            );
            
            -- Order Items table
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                product_name VARCHAR(100),
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                discount_percentage DECIMAL(5,2),
                total_price DECIMAL(10,2),
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
            );
            """
        )


        connection.commit()


def fill_db_from_json() -> None:
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            data: list[dict[str, Any]] = json.load(file)
    except FileNotFoundError:
        print(f"Error: {JSON_PATH} not found.")
        return None

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM customers;")

        for customer in data:
            # 1. Fill customers table
            cursor.execute("""
                INSERT OR IGNORE INTO customers (
                    first_name, last_name, email, phone, address, 
                    city, country, customer_segment, total_orders
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer['first_name'], customer['last_name'], customer['email'],
                customer['phone'], customer['address'], customer['city'],
                customer['country'], customer['customer_segment'], len(customer["orders"])
            ))

            # Get id from the client
            if cursor.lastrowid:
                customer_id = cursor.lastrowid
            else:
                cursor.execute("SELECT customer_id FROM customers WHERE email = ?", (customer['email'],))
                customer_id = cursor.fetchone()[0]

            # 2. Fill orders table
            for order in customer['orders']:
                cursor.execute("""
                    INSERT INTO orders (
                        customer_id, status, shipping_method, shipping_address,
                        shipping_city, shipping_country, total_amount, 
                        payment_method, payment_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    customer_id, order['status'], order['shipping_method'],
                    order['shipping_address'], order['shipping_city'],
                    order['shipping_country'], order['total_amount'],
                    order['payment_method'], order['payment_status']
                ))

                order_id = cursor.lastrowid

                # 3. Fill orders items table
                for item in order['items']:
                    cursor.execute("""
                        INSERT INTO order_items (
                            order_id, product_id, product_name, quantity, 
                            unit_price, discount_percentage, total_price
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        order_id, item['product_id'], item['product_name'],
                        item['quantity'], item['unit_price'],
                        item['discount_percentage'], item['total_price']
                    ))

        connection.commit()

    print(f"✅ Data from {JSON_PATH.name} has been successfully imported!")
    return None

def setup_db() -> None:
    create_tables()
    fill_db_from_json()
    return None

if __name__ == '__main__':
    setup_db()
