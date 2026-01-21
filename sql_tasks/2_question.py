import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "db" / "sqlite.db"

def query_function() -> None:
    # Find all products that were ordered in the last 30 days but haven&#39;t
    # been ordered in the last 7 days. Include the product_id,
    # product_name, total quantity ordered, and the last order date for each product.
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = """
            SELECT
                oi.product_id,
                oi.product_name,
                SUM(oi.quantity) AS total_quantity,
                MAX(o.order_date) AS last_order_date
            FROM order_items oi
            JOIN orders o ON o.order_id = oi.order_id
            GROUP BY oi.product_id, oi.product_name
            HAVING 
                last_order_date >= date('now', '-30 days')
                AND last_order_date < date('now', '-7 days')
            ORDER BY total_quantity DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            print(f"Product - id: {row[0]}, name: {row[1]}, total_quantity: {row[2]}, last_order_date:{row[3]}")

if __name__ == '__main__':
    query_function()
