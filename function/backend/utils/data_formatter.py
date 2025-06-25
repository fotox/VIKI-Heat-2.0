import re

from utils.logging_service import LoggingService

logging = LoggingService()


def extract_datapoints_from_json_with_api(api: str, data: dict) -> dict:
    """
    Dynamically extracts a nested value from a JSON-like structure using a string-based API path.

    The API string must use Python-style key/index access, e.g.:
        "['data']['viewer']['homes'][0]['currentSubscription']"

    This function will parse the string and apply the corresponding steps on
    the `data` object.

    Args:
        api (str): A string representation of the path to access nested JSON data.
           Supports:
               • dictionary keys: ['key']
               • list indices: [0]
        data (dict): The root data dictionary or JSON object to extract from.

    Returns:
        dict:
            The value found at the given path (type depends on content).

    Raises:
        ValueError: If the path cannot be fully resolved (invalid key/index/type).
    """
    keys: list = re.findall(r"\['(.*?)'\]|\[(\d+)\]", api)

    for key_pair in keys:
        key = key_pair[0] if key_pair[0] else int(key_pair[1])
        try:
            data: dict = data[key]
        except (KeyError, IndexError, TypeError):
            logging.error(f"Could not extract data from {key_pair[0]}")
            raise ValueError(f"Path invalid at path: {key}")

    return data
