import ast
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

DATABASE_URI = os.getenv("DATABASE_URL")

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


def fetch_values(table_name: str, description: str, value_column: str):
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:
            query = text(f"SELECT {value_column} FROM {table_name} WHERE description = :description")
            result = connection.execute(query, {"description": description}).fetchone()

            if result:
                return result[0]
            else:
                return None
    except Exception as e:
        return None


def fetch_r4dcb08_sensor_setting() -> dict | None:
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:
            query = text("""
                SELECT
                    s.api_key,
                    s.measuring_position,
                    m.url,
                    m.api,
                    t.description AS tank_description
                FROM
                    sensors s
                JOIN
                    manufacturer m ON s.manufacturer = m.id
                LEFT JOIN
                    tank_settings t ON s.measuring_device = t.id;
            """)
            result = connection.execute(query).fetchall()

        if result:
            connection_data: dict = ast.literal_eval(result[0][3])
            connection_data['port'] = result[0][2]
            return connection_data
        else:
            return None

    except Exception as e:
        return None


def fetch_heat_pipe_setting() -> dict | None:
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:
            query = text("""
                SELECT
                    m.description,
                    h.ip,
                    h.api_key,
                    m.power_factor,
                    m.power_size,
                    h.buffer
                FROM
                    heating_settings h
                JOIN
                    manufacturer m ON h.manufacturer = m.id
            """)
            result = connection.execute(query).fetchall()

        if result:
            heat_pipe_values = [(value[-2], value[-1]) for value in result if "Heizstab" in value[0]]
            return {'pipe_1': heat_pipe_values[0][0], 'pipe_2': heat_pipe_values[1][0], 'pipe_3': heat_pipe_values[2][0],
                    'buffer_1': heat_pipe_values[0][1], 'buffer_2': heat_pipe_values[1][1], 'buffer_3': heat_pipe_values[2][1]}
        else:
            return None

    except Exception as e:
        return None
