import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="Chandu@123"
    )

    print("Database connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    print("PostgreSQL version:")
    print(cursor.fetchone()[0])

    cursor.close()
    connection.close()

    print("Database connection closed.")

except Exception as error:
    print("Database connection failed.")
    print("Error:", error)