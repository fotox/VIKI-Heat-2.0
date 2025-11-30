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
    ALLOWED_TABLES = {
        'manufacturer', 'energy_settings', 'heating_settings', 
        'sensors', 'tank_settings', 'location'
    }
    ALLOWED_COLUMNS = {
        'url', 'api', 'ip', 'api_key', 'price', 'description',
        'manufacturer', 'model_type', 'power_factor', 'power_size'
    }
    
    if table_name not in ALLOWED_TABLES:
        logging.error(f"Invalid table name: {table_name}")
        return None
    
    if value_column not in ALLOWED_COLUMNS:
        logging.error(f"Invalid column name: {value_column}")
        return None
    
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
                    tank_settings t ON s.measuring_device = t.id
                WHERE
                    m.model_type = 'DS18B20'
                LIMIT 1;
            """)
            result = connection.execute(query).fetchone()

        if not result:
            logging.warning("Keine R4DCB08 Temperatursensordaten vorhanden")
            return None

        try:
            api_data = result[3]
            if not api_data:
                logging.error("API-Feld ist leer")
                return None
                
            connection_data: dict = ast.literal_eval(api_data)
            connection_data['port'] = result[2]
            
            required_fields = ['baudrate', 'timeout', 'parity', 'stopbits', 'bytesize']
            for field in required_fields:
                if field not in connection_data:
                    logging.error(f"Erforderliches Feld fehlt: {field}")
                    return None
                    
            return connection_data
            
        except (ValueError, SyntaxError, TypeError) as e:
            logging.error(f"WEITERLEITUNGSFEHLER beim Parsen der API-Daten: {e}")
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
                WHERE
                    m.description LIKE '%Heizstab%'
                ORDER BY h.id
                LIMIT 3;
            """)
            result = connection.execute(query).fetchall()

        if not result:
            logging.warning("Keine Heizstabdaten vorhanden")
            return None

        heat_pipe_config = {}
        
        for idx, row in enumerate(result, start=1):
            try:
                power_factor = row[3] if row[3] is not None else 1.0
                power_size = row[4] if row[4] is not None else 2000
                buffer = row[5] if row[5] is not None else 0
                
                heat_pipe_config[f'pipe_{idx}'] = int(power_factor * power_size)
                heat_pipe_config[f'buffer_{idx}'] = int(buffer)
                
            except (TypeError, ValueError, IndexError) as e:
                logging.error(f"Fehler beim Verarbeiten von Heizstab {idx}: {e}")
                continue
        
        if len(heat_pipe_config) < 2:  # Mindestens 1 Heizstab (pipe_1 + buffer_1 = 2 Einträge)
            logging.warning(f"Nicht genug gültige Heizstabdaten: {len(heat_pipe_config)//2} gefunden")
            return None
            
        return heat_pipe_config

    except (OperationalError, ProgrammingError, InterfaceError, StatementError, DBAPIError, ArgumentError) as e:
        logging.error(f"DATENBANKFEHLER: {e}")
        return None
