import json
import os
import re

import requests
from flask import Response

from database.crud import fetch_value


ACCESS_TOKEN = fetch_value("energy_settings", "Tibber Clouddienst", "api_key")
URL: str = fetch_value("manufacturer", "Tibber Strompreis Info", "url")
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESS_TOKEN
}


def pull_price_info_from_tibber_api() -> json:
    """
    Fetches the current energy price information.
    :return prices: JSON containing the energy price data.
    """
    api: str = fetch_value("manufacturer", "Tibber Strompreis Info", "api")
    keys = re.findall(r"\['(.*?)'\]|\[(\d+)\]", api)
    with open(os.path.join(os.path.dirname(__file__), "graphql\\tibber_price_info.graphql"), "r") as file:
        query: str = file.read()

    response: Response = requests.post(URL, headers=HEADERS, json={'query': query})
    data: json = response.json()

    for key_pair in keys:
        key = key_pair[0] if key_pair[0] else int(key_pair[1])
        try:
            data = data[key]
        except (KeyError, IndexError, TypeError):
            raise ValueError(f"Pfad ungültig an Teil: {key}")

    return data.get("today", []) + data.get("tomorrow", [])


def pull_consume_information_from_tibber_api(config: json) -> json:
    """
    Fetches the current energy price information.

    :param config: Configuration of v.i.k.i-heat

    :return consume: JSON containing the energy price data.
    """
    url: str = config['electricity_provider']['provider']['Tibber']['url']
    with open("common/pull_requests/graphql/tibber_consume_info.graphql", "r") as file:
        query: str = file.read()

    response: Response = requests.post(url, headers=HEADERS, json={'query': query})
    consume: json = response.json()['data']['viewer']['homes'][0]['consumption']['nodes']

    logging.info("Pull energy consume from tibber API")

    return consume
