import os
import ast
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError, ArgumentError, StatementError, DBAPIError, InterfaceError
from dotenv import load_dotenv
from utils.logging_service import LoggingService

DATABASE_URI = os.getenv("DATABASE_URL")
logging = LoggingService()

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


def fetch_values(table_name: str, description: str, value_column: str):
    """
    Retrieves a specific value from a database table based on a description filter.

    Args:
        table_name (str): The name of the table to query.
        description (str): The description value to filter by.
        value_column (str): The name of the column to extract the value from.

    Returns:
        str | None: The matched value from the specified column if found, otherwise None.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If a database error occurs (connection, syntax, etc.).
        TypeError, IndexError: If the result set is not in the expected format.
    """
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:
            query = text(f"SELECT {value_column} FROM {table_name} WHERE description = :description")
            result = connection.execute(query, {"description": description}).fetchone()

            if result:
                return result[0]
            else:
                return None
    except (OperationalError, ProgrammingError, ArgumentError, StatementError, DBAPIError) as e:
        logging.error(f"DATENBANKFEHLER: {e}")
        return None


def fetch_r4dcb08_sensor_setting() -> dict | None:
    """
    Fetches sensor settings for the R4DCB08 measuring device and parses connection parameters.

    Returns:
        dict | None: A dictionary containing parsed connection settings if available,
                     otherwise None.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: On database-related errors.
        ValueError, SyntaxError, TypeError: If the API field contains invalid or malformed data.
        IndexError: If expected result structure is not met.
    """
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
            try:
                connection_data: dict = ast.literal_eval(result[0][3])
                connection_data['port'] = result[0][2]
                return connection_data
            except (ValueError, SyntaxError, TypeError, IndexError) as e:
                logging.error(f"WEITERLEITUNGSFEHLER: {e}")
                return None
        else:
            logging.warning(f"Keine Temperatursensordaten vorhanden")
            return None

    except (OperationalError, ProgrammingError, InterfaceError, StatementError, DBAPIError, ArgumentError) as e:
        logging.error(f"DATENBANKFEHLER: {e}")
        return None


def fetch_heat_pipe_setting() -> dict | None:
    """
    Retrieves heating element and buffer settings for heat pipes from the database.

    Filters only entries containing "Heizstab" in the manufacturer description
    and returns data for the first three entries.

    Returns:
        dict | None: A dictionary with keys 'pipe_1'–'pipe_3' and 'buffer_1'–'buffer_3' if
                     enough valid entries are found, otherwise None.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If any SQL or connection error occurs.
        IndexError, TypeError, AttributeError: If result structure is unexpected or incomplete.
    """
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
            try:
                heat_pipe_values = [
                    (value[-2], value[-1]) for value in result
                    if isinstance(value[0], str) and "Heizstab" in value[0]
                ]

                if len(heat_pipe_values) >= 3:
                    return {
                        'pipe_1': heat_pipe_values[0][0],
                        'pipe_2': heat_pipe_values[1][0],
                        'pipe_3': heat_pipe_values[2][0],
                        'buffer_1': heat_pipe_values[0][1],
                        'buffer_2': heat_pipe_values[1][1],
                        'buffer_3': heat_pipe_values[2][1]
                    }
                else:
                    logging.warning(f"Nicht genug Heizstabdaten vorhanden")
                    return None

            except (IndexError, TypeError, AttributeError) as e:
                logging.error(f"WEITERLEITUNGSFEHLER: {e}")
                return None
        else:
            logging.warning(f"Keine Heizstabdaten vorhanden")
            return None

    except (OperationalError, ProgrammingError, InterfaceError, StatementError, DBAPIError, ArgumentError) as e:
        logging.error(f"DATENBANKFEHLER: {e}")
        return None
