import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "SqlLite.db"

def query_function() -> None:
    # Identifies all customers where their total_orders column
    # doesn't match their actual number of orders in the orders table.
    # Shows both the stored total_orders value and the actual count.
    # Shows the last time their total_orders was updated.
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        query = """
            WITH real_total_orders_count AS (
                SELECT 
                    o.customer_id,
                    MAX(o.order_date) AS last_order_date,
                    COUNT(*) as customer_total_orders_count
                FROM orders o
                GROUP BY o.customer_id
            )
            
            SELECT 
                c.customer_id,
                c.total_orders AS total_orders_count_from_customers_table,
                COALESCE(rtoc.customer_total_orders_count, 0) AS total_orders_count_from_orders_table,
                rtoc.last_order_date
            FROM customers c
            LEFT JOIN real_total_orders_count rtoc ON c.customer_id = rtoc.customer_id
            WHERE total_orders_count_from_customers_table != total_orders_count_from_orders_table
        """
        cursor.execute(query)
        results = cursor.fetchall()

    for row in results:
        print(
            f"Customer - "
            f"customer_id: {row[0]},"
            f" total_orders_count_from_customers_table: {row[1]},"
            f" total_orders_count_from_orders_table: {row[2]},"
            f"last_order_date: {row[3]}"
        )

    return None

if __name__ == '__main__':
    query_function()