import re


def extract_datapoints_from_json_with_api(api: str, data: dict) -> dict:
    """
    Extracts data points from a json file based on api point.
    :param api: List of keys
    :param data: Dict with data from endpoint
    :return: dict with extracted data
    """
    keys: list = re.findall(r"\['(.*?)'\]|\[(\d+)\]", api)

    for key_pair in keys:
        key = key_pair[0] if key_pair[0] else int(key_pair[1])
        try:
            data: dict = data[key]
        except (KeyError, IndexError, TypeError):
            raise ValueError(f"Path invalid at path: {key}")

    return data
