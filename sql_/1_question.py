import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "SqlLite.db"

def query_function() -> None:
    # Find the top 5 customers who have spent the most
    # money across all their orders. Return their name, email, and total spend.
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = """
            SELECT c.first_name, c.last_name, SUM(o.total_amount) as total_spent
            FROM customers as c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            ORDER BY o.total_amount DESC
            LIMIT 5;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            print(f"Customer: {row[0]} ({row[1]}) - Spent: ${row[2]}")

if __name__ == '__main__':
    query_function()
