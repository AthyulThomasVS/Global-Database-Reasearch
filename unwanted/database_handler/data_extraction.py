import mysql.connector
import json
from datetime import datetime

def extract_and_store():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="Aasath@7862", database="usnvd")
        cursor = conn.cursor()
        with open("binlog_events.json", "r") as file:
            data = json.load(file)
        for row in data:
            row_data = row.get("data", {})
            table = row.get("table", "vulnerabilities")
            value_to_check = row_data.get("description")
            cursor.execute("SELECT EXISTS(SELECT 1 FROM vulnerabilities WHERE description = %s)", (value_to_check,))
            exists = cursor.fetchone()[0]
            if exists:
                last_modified_str = row_data.get("last_modified_date")
                if last_modified_str:
                    tmp_date = datetime.strptime(last_modified_str, "%Y-%m-%d %H:%M:%S")
                    cursor.execute("SELECT last_modified_date FROM vulnerabilities WHERE id = %s", (row_data.get("id"),))
                    result = cursor.fetchone()
                    if result and result[0] and tmp_date > result[0]:
                        cursor.execute("UPDATE vulnerabilities SET last_modified_date = %s WHERE id = %s", (tmp_date, row_data.get("id")))
                        print(f"Updated {row_data.get('id')} with new last_modified_date: {tmp_date}")
                        conn.commit()
            else:
                if 'id' in row_data:
                    del row_data['id']
                columns = ", ".join(row_data.keys())
                placeholders = ", ".join(["%s"] * len(row_data))
                values = tuple(row_data.values())
                cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
                print("Data inserted successfully!")
                conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
