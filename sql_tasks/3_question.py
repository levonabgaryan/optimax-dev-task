import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "db" / "sqlite.db"

def query_function() -> None:
    # For each customer, show their total spend and how it compares to the
    # average spend in their city. Include their name, city, total spend,
    # and city average spend. Only include cities that have at least 2 customers.
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        query = """
                WITH city_stats AS (
                    SELECT
                        c.city,
                        AVG(o.total_amount) AS city_avg
                    FROM customers c
                    JOIN orders o ON c.customer_id = o.customer_id
                    GROUP BY (c.city)
                    HAVING COUNT(DISTINCT c.customer_id) >= 2
                )

                SELECT
                    c.first_name,
                    c.last_name,
                    c.city,
                    SUM(o.total_amount) AS total_spend,
                    cs.city_avg
                FROM customers c
                JOIN orders o ON o.customer_id = c.customer_id
                JOIN city_stats cs ON c.city = cs.city
                GROUP BY c.customer_id, c.first_name, c.last_name, c.city
                ORDER BY total_spend DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

    for row in results:
        print(
            f"Customer - first_name: {row[0]}, last_name: {row[1]}, city: {row[2]}, total_spend: {row[3]} city_avg_amount: {row[4]}"
        )

    return None

if __name__ == '__main__':
    query_function()