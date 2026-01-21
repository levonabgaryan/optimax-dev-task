import json
import sqlite3
from pathlib import Path
from typing import Any
import base64

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "SqlLite.db"
print(DB_PATH)


def convert_pub_sub_message_to_dict(message: str) -> dict[str, Any]:
    # https://docs.cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage#:~:text=%7B%0A%20%20%22data%22%3A%20string%2C%0A%20%20%22attributes%22%3A%20%7B%0A%20%20%20%20string%3A%20string%2C%0A%20%20%20%20...%0A%20%20%7D%2C%0A%20%20%22messageId%22%3A%20string%2C%0A%20%20%22publishTime%22%3A%20string%2C%0A%20%20%22orderingKey%22%3A%20string%0A%7D
    message: dict[str, Any] = json.loads(message)
    if 'data' not in message:
        print("Message doesn't have data ")
        raise

    # Decode base64 string to raw bytes
    real_bytes: bytes = base64.b64decode(message['data'])

    # Convert bytes to a string
    json_string: str = real_bytes.decode()

    # Parse JSON string into a Python dictionary
    data = json.loads(json_string)

    print(f"data: {data}")
    return data

def save_data_to_db(data: dict[str, Any]) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        query = """
            INSERT INTO customers (first_name, last_name, email, phone, address, city, country, customer_segment) VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            data.get("first_name"),
            data.get("last_name"),
            data.get("email"),
            data.get("phone"),
            data.get("address"),
            data.get("city"),
            data.get("country"),
            data.get("customer_segment")
        )

        cursor.execute(query, params)
        connection.commit()
        print("Data has been successfully saved in db")

    return None

