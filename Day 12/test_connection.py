from config import get_database_engine

try:
    engine = get_database_engine()

    with engine.connect() as connection:
        print("PostgreSQL connection successful!")
        print("Connected database:", connection.engine.url.database)

    engine.dispose()

except Exception as error:
    print("Database connection failed!")
    print(error)