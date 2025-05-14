import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

DATABASE_URI = os.getenv("DATABASE_URL")

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


def fetch_value(table_name: str, description: str, value_column: str):
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
