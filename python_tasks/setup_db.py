import sqlite3
from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent
DB_PATH: Final[Path] = BASE_DIR / "db" / "sqlite.db"


def create_customers_table() -> None:
    # This function create a SqlLite db file and customers table.
    # Db uses just for saving data which coming from a json-.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        connection.executescript(
            """
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
            """
        cursor.executescript(query)
        connection.commit()

    print("✅ Customers table have been created")


if __name__ == '__main__':
    create_customers_table()