import time

from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.pdu import ModbusPDU

from database.fetch_data import fetch_r4dcb08_sensor_setting


def read_temp_sensors_from_r4dcb08(temp_sensor_data: dict) -> dict:
    """
    Read temperature measure values from R4DCB08 module.
    :param: sensor_id: List of ports of R4DCB08 who is locked the temperature sensor
    :return: Dict of temperature values.
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
        print(f"Error by reading sensor: {e}")

    finally:
        client.close()

    return temp_sensor_data


def get_temp_of_tank_with_heat_pipe(temp_sensors: dict, tanks: dict) -> tuple[float, float]:
    """
    Load data from tank with heat pipe and return the tank name and the actual destination temperature.
    :param temp_sensors: config of viki-heat for temperature sensors.
    :param tanks: config of viki-heat for tanks.
    :return: tank name and actual destination temperature.
    """
    used_tank: str = ""
    destination_temp: float = 0.0

    for tank_type in tanks:
        if tanks[tank_type]["heating_element"]:
            used_tank: str = tank_type
            destination_temp: float = tanks[tank_type]["destination_temp"]

    for sensors in temp_sensors:
        if temp_sensors[sensors]["binding"].startswith(used_tank):
            return float(temp_sensors[sensors]["value"]), destination_temp

    return 0.0, 0.0
