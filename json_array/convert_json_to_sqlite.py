import sqlite3
import json

# Function to insert data into the database while ensuring unique descriptions
def insert_data_from_json(json_file):
    # Open a new connection to the SQLite database
    conn = sqlite3.connect('jsonconvert.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS vulnerabilities (
                        id INTEGER PRIMARY KEY,
                        description TEXT UNIQUE,
                        severity TEXT,
                        published_date TEXT,
                        last_modified_date TEXT
                    )''')

    # Read data from the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Loop through each record in the JSON data
    for record in data:
        # Access the 'data' key and get the fields inside it
        data = record.get("data", {})  # Use get to handle missing 'data' key
        id_ = data.get("id")  # Use get to handle missing 'id' key
        description = data.get("description", "No Description").strip()  # Default value if description is missing
        severity = data.get("severity")
        published_date = data.get("published_date")
        last_modified_date = data.get("last_modified_date")

        try:
            # Try to insert the new record into the database
            cursor.execute('''INSERT OR IGNORE INTO vulnerabilities (id, description, severity, published_date, last_modified_date)
                              VALUES (?, ?, ?, ?, ?)''', (id_, description, severity, published_date, last_modified_date))
            print(f"Inserting record with description: {description}")
        except sqlite3.IntegrityError:
            # If a description is already present, it will be skipped due to UNIQUE constraint
            print(f"Description '{description}' has already been inserted. Skipping this record.")

    # Commit the changes
    conn.commit()

    # Close the connection after commit
    conn.close()

# Specify the path to your JSON file (updated to 'sample.json')
json_file_path = 'sample.json'

# Call the function to insert data from the JSON file into the database
insert_data_from_json(json_file_path)

# To verify that data is inserted, open a new connection to query the data
conn = sqlite3.connect('jsonconvert.db')
cursor = conn.cursor()

# Fetch the data
cursor.execute("SELECT * FROM vulnerabilities")
rows = cursor.fetchall()

# Print the inserted data
print("\nFinal state of the database:")
for row in rows:
    print(row)

# Close the connection
conn.close()
