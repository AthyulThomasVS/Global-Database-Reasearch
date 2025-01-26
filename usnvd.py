import json
import mysql.connector
from datetime import datetime
# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",         # Replace with your host
    user="root",          # Replace with your MySQL username
    password="Aasath@7862",      # Replace with your MySQL password
    database="usnvd"         # Replace with your database name
)
cursor = conn.cursor()

# Load JSON file
with open("usnvd.json") as f:
    data = json.load(f)

# Insert data into the database
for item in data['vulnerabilities']:
    cve_id = item['id']
    description = item['description']
    published_date_str = item['published_date']
    last_modified_date_str = item['last_modified_date']
    severity = item.get('severity', None)
    published_date = datetime.strptime(published_date_str, "%Y-%m-%dT%H:%M:%SZ")
    last_modified_date = datetime.strptime(last_modified_date_str, "%Y-%m-%dT%H:%M:%SZ")
    # Insert into vulnerabilities table
    cursor.execute("""
        INSERT INTO vulnerabilities (id, description, severity, published_date, last_modified_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (cve_id, description, severity, published_date, last_modified_date))

# Commit the transaction to save changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data successfully inserted into the MySQL database!")
