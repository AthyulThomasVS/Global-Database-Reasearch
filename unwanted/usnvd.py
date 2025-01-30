import mysql.connector
import time

BINLOG_FILE = 'AASATH-bin.000048'  # Update with your log file name
BINLOG_POSITION = 0  # Start from the beginning (adjust this as needed)

def extract_row_data(event):
    """Helper function to extract row data from binlog event."""
    event_type = event[2]
    
    # Handle INSERT, UPDATE, and DELETE events
    if event_type == 'Write_rows':
        # Extract and display inserted rows
        print("Inserted Rows:")
        for row in event[5]:
            print(row)
    elif event_type == 'Update_rows':
        # Extract and display updated rows (before and after)
        print("Updated Rows:")
        for row in event[5]:
            print(f"Before: {row[0]} | After: {row[1]}")
    elif event_type == 'Delete_rows':
        # Extract and display deleted rows
        print("Deleted Rows:")
        for row in event[5]:
            print(row)

def process_binlog_events():
    """Function to read binlog events and extract data."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Aasath@7862',
        database='usnvd'
    )
    
    cursor = connection.cursor()
    
    # Fetch binlog events starting from the provided log file and position
    cursor.execute(f"SHOW BINLOG EVENTS IN '{BINLOG_FILE}' FROM {BINLOG_POSITION}")

    for event in cursor:
        # Check if the event is a CRUD operation
        if event[2] in ['Write_rows', 'Update_rows', 'Delete_rows']:
            extract_row_data(event)
    
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

# Poll for changes in the binlog
def poll_for_changes():
    while True:
        try:
            process_binlog_events()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)  # Wait for a few seconds before checking again

# Start the process
poll_for_changes()
