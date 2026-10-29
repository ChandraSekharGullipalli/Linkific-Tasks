
import requests
import psycopg2
import os

from psycopg2.extras import execute_values

API_URL = "https://jsonplaceholder.typicode.com/users"


def extract_data():
    """Extract user records from the API."""
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("The API did not return a list.")

    print(f"Extracted {len(data)} records from API.")
    return data


def transform_data(users):
    """Select and validate the required fields."""
    transformed = []

    for user in users:
        if not user.get("id") or not user.get("email"):
            continue

        transformed.append((
            user["id"],
            user.get("name", ""),
            user.get("username", ""),
            user["email"],
            user.get("phone", ""),
            user.get("website", ""),
            user.get("address", {}).get("city", ""),
            user.get("company", {}).get("name", "")
        ))

    print(f"Transformed {len(transformed)} valid records.")
    return transformed


def load_data(records):
    """Load records into PostgreSQL."""
    connection = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "postgres"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.environ["PGPASSWORD"]
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS api_users (
                        user_id INTEGER PRIMARY KEY,
                        name VARCHAR(150),
                        username VARCHAR(100),
                        email VARCHAR(200),
                        phone VARCHAR(100),
                        website VARCHAR(150),
                        city VARCHAR(100),
                        company VARCHAR(150)
                    )
                """)

                execute_values(cursor, """
                    INSERT INTO api_users (
                        user_id, name, username, email,
                        phone, website, city, company
                    )
                    VALUES %s
                    ON CONFLICT (user_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        username = EXCLUDED.username,
                        email = EXCLUDED.email,
                        phone = EXCLUDED.phone,
                        website = EXCLUDED.website,
                        city = EXCLUDED.city,
                        company = EXCLUDED.company
                """, records)

                cursor.execute("SELECT COUNT(*) FROM api_users")
                total = cursor.fetchone()[0]

        print(f"Loaded {len(records)} records into PostgreSQL.")
        print(f"Total records currently in api_users: {total}")

    finally:
        connection.close()


def main():
    try:
        users = extract_data()
        records = transform_data(users)

        if records:
            load_data(records)
        else:
            print("No valid records to load.")

    except (requests.RequestException, ValueError) as error:
        print(f"API or data validation error: {error}")
    except (psycopg2.Error, KeyError) as error:
        print(f"Database or configuration error: {error}")


if __name__ == "__main__":
    main()
