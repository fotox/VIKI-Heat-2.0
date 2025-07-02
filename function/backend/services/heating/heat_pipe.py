from database.fetch_data import fetch_heat_pipe_setting
from services.heating.helper import load_memory, toggle_all_relais, read_sensors_by_tank_with_heat_pipe, toogle_relay
from utils.logging_service import LoggingService

logging = LoggingService()


def automatic_control(cover: int):
    memory: dict = load_memory()
    mode: str = memory.get("mode")
    heat_pipes_range: list = range(1, len(memory.get("heat_pipes")) + 1)

    if mode == "Manuell":
        pass

    if mode == "Urlaub":
        logging.debug("[URLAUB] Modus aktiv")
        toggle_all_relais(False)
        pass

    sensors: dict = read_sensors_by_tank_with_heat_pipe()
    temp: float = sensors.get("tank")[2]
    dest_temp: float = sensors.get("dest_temp", 0.0)

    if mode == "Schnell heizen":
        logging.debug("[SCHNELLHEIZEN] Modus aktiv")
        if temp >= dest_temp:
            logging.debug("[SCHNELLHEIZEN] Zieltemperatur erreicht")
            toggle_all_relais(False)
        else:
            logging.debug("[SCHNELLHEIZEN] Zieltemperatur nicht erreicht")
            toggle_all_relais(True)
        pass

    heat_pipe_config: dict = fetch_heat_pipe_setting()

    if mode == "Automatik":
        logging.debug("[AUTOMATIK] Modus aktiv")
        if temp < dest_temp:

            for pipe_number in heat_pipes_range:
                phase = heat_pipe_config.get(f"pipe_{pipe_number}")
                buffer = heat_pipe_config.get(f"buffer_{pipe_number}")
                logging.debug(f"[Automatic mode] Cover: {cover} | Phase {pipe_number}: {phase} + {buffer}")

                if cover > phase + buffer:
                    new_state = toogle_relay(pipe_number, True)
                    if not new_state:
                        pass
                    cover -= (phase + buffer)

                elif cover < 0:
                    new_state = toogle_relay(pipe_number, False)
                    if not new_state:
                        pass

        else:
            logging.debug("[AUTOMATIK] Temperatur erreicht")
            toggle_all_relais(False)
            pass
