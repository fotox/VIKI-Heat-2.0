import requests
from flask import Response
from pathlib import Path

from database.fetch_data import fetch_values
from utils.data_formatter import extract_datapoints_from_json_with_api
from utils.logging_service import LoggingService

logging = LoggingService()


def pull_price_info_from_tibber_api() -> list:
    """
    Retrieves spot-price data from the Tibber GraphQL API.

    Returns:
        list[dict]: Concatenated list ``today + tomorrow`` – i.e.
        • every hourly price for **today**
        • all prices **up to 13:00** for **tomorrow**

        Each element is whatever structure the parser returns (typically ``{"time": "...", "price": 0.123}``).

        ``[]`` (empty list) is returned if the GraphQL file is missing *or* the HTTP request fails.

    Notes:
        - Uses the shared ``ACCESS_TOKEN`` and ``HEADERS`` constants.
        - Any ``requests.RequestException`` is swallowed and mapped to ``[]``.
    """
    url: str = fetch_values("manufacturer", "Tibber Strompreis Info", "url")
    
    if not url:
        logging.error("[Tibber] URL not found in database")
        return []
    
    try:
        graphql_path = Path(__file__).parent / "graphql" / "tibber_price_info.graphql"
        with open(graphql_path, "r") as file:
            query: str = file.read()

        response: Response = requests.post(url, headers=load_tibber_auth(), json={'query': query})
        api: str = fetch_values("manufacturer", "Tibber Strompreis Info", "api")
        
        if not api:
            logging.error("[Tibber] API path not found in database")
            return []
        
        data: dict = extract_datapoints_from_json_with_api(api, response.json())

    except FileNotFoundError as fnfe:
        logging.error(f"Error by open file: {fnfe}")
        return []
    except requests.exceptions.HTTPError as errh:
        logging.error(f"Error by http request: {errh}")
        return []

    return data.get("today", []) + data.get("tomorrow", [])


def pull_consume_information_from_tibber_api() -> float:
    """
    Calculates the household's electricity consumption over the **last 24 h**
    using Tibber’s *consumption* GraphQL endpoint.

    Returns:
        float: Total energy consumed in the past 24 hours (unit determined by the API, usually **kWh**).
        If the request or parsing fails, the function still returns a numeric value (0.0) because an empty result list
        sums to **0.0**.

    Raises:
        FileNotFoundError: If the GraphQL query file cannot be located.
        RequestException: If the HTTP request encounters an error.
        KeyError / TypeError: If the expected ``"consumption"`` key is missing or malformed in the parsed data.
    """
    try:
        url: str = fetch_values("manufacturer", "Tibber Stromverbrauch", "url")
        api: str = fetch_values("manufacturer", "Tibber Stromverbrauch", "api")
        
        if not url or not api:
            logging.error("[Tibber] Configuration incomplete in database")
            return 0.0

    except Exception as err:
        logging.error(f"[Tibber] DB-Lookup failed: {err}")
        return 0.0

    try:
        graphql_path = Path(__file__).parent / "graphql" / "tibber_consume_info.graphql"
        with open(graphql_path, "r", encoding="utf-8") as file:
            query: str = file.read()

    except FileNotFoundError as fnfe:
        logging.error(f"[Tibber] GraphQL-file not found: {fnfe}")
        return 0.0

    except OSError as ose:
        logging.error(f"[Tibber] Error by reading GraphQL-file: {ose}")
        return 0.0

    try:
        response: Response = requests.post(url, headers=load_tibber_auth(), json={"query": query}, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as rex:
        logging.error(f"[Tibber] HTTP-Error: {rex}")
        return 0.0

    try:
        data: dict = extract_datapoints_from_json_with_api(api, response.json())

    except (ValueError, KeyError, TypeError) as parse_err:
        logging.error(f"[Tibber] Error by parsing the api-request: {parse_err}")
        return 0.0

    try:
        return sum(item["consumption"] for item in data)

    except (KeyError, TypeError) as calc_err:
        logging.error(f"[Tibber] Invalid data format: {calc_err}")
        return 0.0


def load_tibber_auth() -> dict:
    access_token = fetch_values("energy_settings", "Tibber Clouddienst", "api_key")
    
    if not access_token:
        logging.error("[Tibber] API key not found in database")
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '
        }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    return headers
