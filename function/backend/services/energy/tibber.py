import os
import requests
from flask import Response

from database.fetch_data import fetch_values
from services.helper import extract_datapoints_from_json_with_api

ACCESS_TOKEN = fetch_values("energy_settings", "Tibber Clouddienst", "api_key")
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESS_TOKEN
}


def pull_price_info_from_tibber_api() -> list:
    """
    Fetches the current energy price information.
    :return prices: Energy price data for today and at 13 o'clock for tomorrow.
    """
    url: str = fetch_values("manufacturer", "Tibber Strompreis Info", "url")

    try:
        with open(os.path.join(os.path.dirname(__file__), "graphql\\tibber_price_info.graphql"), "r") as file:
            query: str = file.read()

        response: Response = requests.post(url, headers=HEADERS, json={'query': query})
        api: str = fetch_values("manufacturer", "Tibber Strompreis Info", "api")
        data: dict = extract_datapoints_from_json_with_api(api, response.json())

    except FileNotFoundError as fnfe:
        print(f"Error by open file: {fnfe}")
        return []
    except requests.exceptions.HTTPError as errh:
        print(f"Error by http request: {errh}")
        return []

    return data.get("today", []) + data.get("tomorrow", [])


def pull_consume_information_from_tibber_api() -> float:
    """
    Fetches the current energy price information.
    :return consume: Sum of consume the last 24 hours
    """
    url: str = fetch_values("manufacturer", "Tibber Stromverbrauch", "url")
    with open("common/pull_requests/graphql/tibber_consume_info.graphql", "r") as file:
        query: str = file.read()

    response: Response = requests.post(url, headers=HEADERS, json={'query': query})
    api: str = fetch_values("manufacturer", "Tibber Stromverbrauch", "api")
    data: dict = extract_datapoints_from_json_with_api(api, response.json())

    return sum([consume['consumption'] for consume in data])
