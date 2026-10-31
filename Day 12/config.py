
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

def get_database_engine():

    db_password = os.getenv("DB_PASSWORD")

    if not db_password:
        raise ValueError("Database password is missing in .env file")

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=db_password,
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "etl_database")
    )

    engine = create_engine(connection_url)

    return engine
