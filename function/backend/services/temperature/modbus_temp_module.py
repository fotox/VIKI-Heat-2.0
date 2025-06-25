import time

from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.pdu import ModbusPDU

from database.fetch_data import fetch_r4dcb08_sensor_setting
from utils.logging_service import LoggingService

logging = LoggingService()


def read_temp_sensors_from_r4dcb08(temp_sensor_data: dict) -> dict:
    """
    Reads up-to-date temperature values from an *R4DCB08* Modbus-RTU module and updates the provided sensor cache.

    Args:
        temp_sensor_data : dict[int, float]
            A mapping *{sensor_index: last_value}* that will be **updated in place**.
            Indices must be 0–5.

    Returns:
        dict[int, float]
            The same dictionary instance with any successfully read channels overwritten. If the serial connection cannot
            be established or a read error occurs, the original values are returned unchanged.
    """

    client_con_data: dict = fetch_r4dcb08_sensor_setting()
    client = ModbusClient(
        port=client_con_data['port'],
        baudrate=client_con_data['baudrate'],
        timeout=client_con_data['timeout'],
        parity=client_con_data['parity'],
        stopbits=client_con_data['stopbits'],
        bytesize=client_con_data['bytesize']
    )

    if not client.connect():
        return temp_sensor_data

    try:
        response: ModbusPDU = client.read_holding_registers(0x0000, 8, slave=1)
        if not response.isError():
            temperatures: list[int] = response.registers
            for i, temp in enumerate(temperatures[:6]):
                if temp < 30000:
                    if i in temp_sensor_data.keys():
                        temp_sensor_data[i] = temp / 10.0
            client.close()
            return temp_sensor_data

    except Exception as e:
        logging.error(f"Error by reading sensor: {e}")

    finally:
        client.close()

    return temp_sensor_data


def get_temp_of_tank_with_heat_pipe(temp_sensors: dict, tanks: dict) -> tuple[float, float]:
    """
    Determines the current temperature of the tank that has an active heating element and returns it together with that
    tank’s destination temperature.

    Args:
        temp_sensors : dict[str, dict]
            Viki-Heat sensor configuration, e.g.
            ``{"sensor1": {"binding": "tank_a_top", "value": 55.3}, ...}``
        tanks : dict[str, dict]
            Viki-Heat tank configuration, e.g.
            ``{"tank_a": {"heating_element": True, "destination_temp": 60.0}, ...}``

    Returns:
        tuple[float, float]
            ``(current_temp, destination_temp)`` in **°C**.
            If no matching tank/sensor is found, ``(0.0, 0.0)`` is returned.

    Raises:
        None – the function is designed to fall back to ``0.0`` values rather than raise.
    """
    try:
        used_tank = next(
            name for name, cfg in tanks.items() if cfg.get("heating_element")
        )
        destination_temp = float(tanks[used_tank]["destination_temp"])

    except (StopIteration, KeyError, TypeError, ValueError) as tank_err:
        logging.error(f"[HeatPipe] tank searching invalid: {tank_err}")
        return 0.0, 0.0

    try:
        for s_cfg in temp_sensors.values():
            if s_cfg.get("binding", "").startswith(used_tank):
                return float(s_cfg["value"]), destination_temp
    except (KeyError, TypeError, ValueError) as sensor_err:
        logging.error(f"[HeatPipe] Sensor reading invalid: {sensor_err}")
        return 0.0, 0.0

    return 0.0, destination_temp
