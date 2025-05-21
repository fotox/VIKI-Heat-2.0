import time

from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.pdu import ModbusPDU

from database.crud import fetch_r4dcb08_sensor_setting


def read_temp_sensors_from_r4dcb08(sensor_ids: dict) -> dict:
    """
    Read temperature measure values from R4DCB08 module.
    :param: sensor_id: List of ports of R4DCB08 who is locked the temperature sensor
    :return: Dict of temperature values.
    """
    temp_sensor_data: dict = dict.fromkeys(list(range(0, 7)))
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
                    temp_sensor_data[i] = temp / 10.0
            client.close()
            return temp_sensor_data

    except Exception as e:
        print(f"Error by reading sensor: {e}")

    finally:
        client.close()
