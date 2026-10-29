
import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="Chandu@123"
    )

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS day10_employees (
        employee_id INT PRIMARY KEY,
        employee_name VARCHAR(100) NOT NULL,
        department VARCHAR(50),
        salary NUMERIC(10, 2)
    );
    """

    cursor.execute(create_table_query)
    connection.commit()

    print("Employee table created successfully!")

    cursor.close()
    connection.close()

except Exception as error:
    print("Error:", error)
