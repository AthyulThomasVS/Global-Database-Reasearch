import mysql.connector
from mysql.connector import Error

def create_database_and_tables():
    try:
        # Connect to MySQL server (without specifying a database)
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,             # Specify port separately
            user='root',           # Change to your MySQL username
            password='mysql01'     # Change to your MySQL password
        )

        if conn.is_connected():
            print("Connected to MySQL server")

            # Create a cursor object
            cursor = conn.cursor()

            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS sourcedb")
            print("Database 'sourcedb' created or already exists.")

            # Select the database
            cursor.execute("USE sourcedb")

            # Create 'vulnerabilities' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id varchar(100),
                    description VARCHAR(100) NOT NULL,
                    published DATETIME NOT NULL,
                    severity float
                );
            ''')
            print("'vulnerabilities' table created or already exists.")

            # Commit the changes
            conn.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

# Call the function to create database and tables
create_database_and_tables()
