import mysql.connector
import json
from datetime import datetime

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aasath@7862",
        database="usnvd"
    )

    if conn.is_connected():
        print("Connected to MySQL database")

    cursor = conn.cursor()

    # Load JSON data
    with open("binlog_events.json", "r") as file:
        data = json.load(file)

    for row in data:
        row_data = row.get("data", {})
        table = row.get("table", "vulnerabilities")  # Default to vulnerabilities table
        # Check if the record exists
        value_to_check = row_data.get("description")
        cursor.execute("SELECT EXISTS(SELECT 1 FROM vulnerabilities WHERE description = %s)", (value_to_check,))
        exists = cursor.fetchone()[0]
        is_present = bool(exists)

        if is_present:
            last_modified_str = row_data.get("last_modified_date")

            if last_modified_str:
                try:
                    tmp_date = datetime.strptime(last_modified_str, "%Y-%m-%d %H:%M:%S")

                    cursor.execute("SELECT last_modified_date FROM vulnerabilities WHERE id = %s", 
                                   (row_data.get("id"),))
                    result = cursor.fetchone()

                    if result and result[0]:
                        last_modified_date = result[0]

                        if tmp_date > last_modified_date:
                            cursor.execute(
                                "UPDATE vulnerabilities SET last_modified_date = %s WHERE id = %s",
                                (tmp_date, row_data.get("id"))
                            )
                            print(f"Updated {row_data.get('id')} with new last_modified_date: {tmp_date}")
                            conn.commit()
                except ValueError:
                    print(f"Skipping invalid date format: {last_modified_str}")
            else:
                print("No date provided.")
        else:
            columns = ", ".join(row_data.keys())
            placeholders = ", ".join(["%s"] * len(row_data))  
            values = tuple(row_data.values())

            insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(insert_query, values)  
            print("Data inserted successfully!")
            conn.commit()

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
