import base64
import json
from typing import Any

from implementation import convert_pub_sub_message_to_dict, save_data_to_db


def create_pub_sub_message_data(data_: dict[str, Any]) -> str:
    # Creates a json-string for pub/sub message
    json_string_data: str = json.dumps(data_)
    raw_bytes_data: bytes = json_string_data.encode()

    # Convert simple bytes to base64 bytes
    base64_string_data: bytes = base64.b64encode(raw_bytes_data)

    return base64_string_data.decode()

if __name__ == '__main__':
    # given
    test_customer_data = {
        "first_name": "Ann",
        "last_name": "Brown",
        "email": "test@mail.com",
        "phone": "test_phone_number",
        "address": "test_address",
        "city": "test_city",
        "country": "test_country",
        "customer_segment": "test_customer_segment"
    }

    pub_sub_message = {
        "data": create_pub_sub_message_data(test_customer_data)
    }

    data = convert_pub_sub_message_to_dict(json.dumps(pub_sub_message))

    # when
    save_data_to_db(data)
