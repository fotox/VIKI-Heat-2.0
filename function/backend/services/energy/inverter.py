from sqlalchemy import select, join
import requests
from flask import Response
from requests.exceptions import RequestException, Timeout, ConnectionError
from sqlalchemy.sql.selectable import GenerativeSelect

from extensions import db
from database.settings import ManufacturerSetting, EnergySetting
from services.heating.heat_pipe import automatic_control
from utils.data_formatter import extract_datapoints_from_json_with_api
from utils.logging_service import LoggingService

logging = LoggingService()


def get_manufacturer_with_energy_settings():
    """
    Retrieves the first manufacturer marked with the notice **"Livedaten"** together with its (optional)
    energy-specific settings.

    Returns:
        dict: A mapping with the keys
            - url (str):   REST endpoint path on the inverter (e.g. "/api/v1/live")
            - api (str):   Name of the parser profile to use for the inverter JSON
            - ip (str):    IPv4/hostname of the inverter (can be ``None`` if not set)
            - price (Any): Latest electricity price stored for this manufacturer/inverter
              (type depends on your DB schema, often ``Decimal`` or ``float``)

        None: If **no** manufacturer with the notice *"Livedaten"* is found.
    """
    stmt: GenerativeSelect = (
        select(
            ManufacturerSetting.url,
            ManufacturerSetting.api,
            ManufacturerSetting.notice,
            EnergySetting.ip,
            EnergySetting.price
        )
        .select_from(
            join(ManufacturerSetting, EnergySetting, ManufacturerSetting.id == EnergySetting.manufacturer, isouter=True)
        )
        .where(ManufacturerSetting.notice == 'Livedaten')
        .limit(1)
    )

    result = db.session.execute(stmt).fetchone()
    if result:
        return {
            "url": result.url,
            "api": result.api,
            "ip": result.ip,
            "price": result.price
        }
    else:
        return None


def pull_live_data_from_inverter():
    """
    Pulls one snapshot of live production / consumption data from the configured inverter and triggers automatic
    heat-pipe control.

    Returns:
        dict: On success, a JSON-serialisable mapping

            {
                "consume": int,
                "production": int,
                "cover": int,
                "accu_capacity": float
            }

        {}: An empty dict if no inverter configuration could be found.

    Raises:
        RequestException: If the HTTP request to the inverter fails.
        ValueError:       If the response body is not valid JSON.
    """
    inverter_data: dict | None = get_manufacturer_with_energy_settings()
    if inverter_data is None:
        logging.warning("[Inverter] No configuration found – returning empty dict")
        return {}

    url: str = f"http://{inverter_data['ip']}{inverter_data['url']}"

    try:
        response: Response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (Timeout, ConnectionError, RequestException) as http_err:
        logging.error(f"[Inverter] HTTP error for {url}: {http_err}")
        return {}

    try:
        raw_json: dict = response.json()
    except ValueError as json_err:
        logging.error(f"[Inverter] Invalid JSON from {url}: {json_err}")
        return {}

    try:
        data: dict = extract_datapoints_from_json_with_api(
            inverter_data["api"], raw_json
        )
    except ValueError as parse_err:
        logging.error(f"[Inverter] API path parsing failed: {parse_err}")
        return {}

    consume: int = round(-data.get("P_Load", 0.0) or 0.0, 0)
    production: int = round(data.get("P_PV", 0.0) or 0.0, 0)
    cover: int = round(-data.get("P_Grid", 0.0) or 0.0, 0)
    accu_capacity: float = round(data.get("P_Akku", 0.0) or 0.0, 1)

    try:
        automatic_control(cover)
    except Exception as ctrl_err:
        logging.warning(f"[HeatPipe] automatic_control failed: {ctrl_err}")

    return {
        "consume": int(consume),
        "production": int(production),
        "cover": int(cover),
        "accu_capacity": float(accu_capacity),
    }
