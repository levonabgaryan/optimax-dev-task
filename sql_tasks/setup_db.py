import sqlite3
from pathlib import Path
from typing import Final


BASE_DIR: Final[Path] = Path(__file__).resolve().parent
DB_PATH: Final[Path] = BASE_DIR / "db" / "sqlite.db"


def create_tables() -> None:
    # This function create a SqlLite db file, run migrations
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        connection.execute("PRAGMA foreign_keys = ON;")

        connection.executescript(
            """
            DROP TABLE IF EXISTS order_items;
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS customers;
            """
        )
        connection.commit()

        query = """
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
        cursor.executescript(query)
        connection.commit()


def fill_db() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        cursor = connection.cursor()

        query = """
        INSERT INTO customers (customer_id, first_name, last_name, email, city, total_orders) VALUES 
            (1, 'John', 'Doe', 'john@test.com', 'New York', 100),
            (2, 'Bob', 'Brown', 'bob@test.com', 'New York', 1),
            (3, 'Eve', 'White', 'eve@test.com', 'New York', 1),
            (4, 'Alice', 'Smith', 'alice@test.com', 'London', 1),
            (5, 'Charlie', 'Davis', 'charlie@test.com', 'London', 1);
            
        INSERT INTO orders (order_id, customer_id, total_amount, order_date) VALUES 
            (1, 1, 500.00, datetime('now', '-10 days')),
            (2, 2, 300.00, datetime('now', '-8 days')),
            (3, 4, 150.00, datetime('now', '-1 day')),
            (4, 5, 250.00, datetime('now', '-2 days'));
        
        INSERT INTO order_items (order_id, product_id, product_name, quantity) VALUES 
            (1, 500, 'Vintage Camera', 1),
            (2, 501, 'Tripod', 1),
            (3, 600, 'Modern Phone', 1);
        """

        cursor.executescript(query)
        connection.commit()

    print(f"✅ Data has been successfully imported!")
    return None

def setup_db() -> None:
    create_tables()
    fill_db()
    return None

if __name__ == '__main__':
    setup_db()
