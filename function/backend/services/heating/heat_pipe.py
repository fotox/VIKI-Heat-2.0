from database.fetch_data import fetch_heat_pipe_setting
from services.heating.helper import load_memory, toggle_all_relais, read_sensors_by_tank_with_heat_pipe, toogle_relay
from utils.logging_service import LoggingService

logging = LoggingService()

DEV_MODE: bool = True


def automatic_control(cover: int):
    memory: dict = load_memory()
    mode: str = memory.get("mode")
    heat_pipes_range: list = range(1, len(memory.get("heat_pipes")) + 1)

    if mode == "Manuell":
        pass

    if mode == "Urlaub":
        toggle_all_relais(False)
        pass

    sensors: dict = read_sensors_by_tank_with_heat_pipe()
    temp: float = sensors.get("tank")[2]
    dest_temp: float = sensors.get("dest_temp", 0.0)

    if mode == "Schnell heizen":
        if temp >= dest_temp:
            toggle_all_relais(False)
        else:
            toggle_all_relais(True)
        pass

    heat_pipe_config: dict = fetch_heat_pipe_setting()

    if mode == "Automatik":
        if temp < dest_temp:

            for pipe_number in heat_pipes_range:
                phase = heat_pipe_config.get(f"pipe_{pipe_number}")
                buffer = heat_pipe_config.get(f"buffer_{pipe_number}")

                if cover > (phase + buffer):
                    new_state = toogle_relay(pipe_number, True)
                    if not new_state:
                        pass
                    if DEV_MODE:
                        cover -= (phase + buffer)

                elif cover < 0:
                    new_state = toogle_relay(pipe_number, False)
                    if not new_state:
                        pass

        else:
            toggle_all_relais(False)
            pass
