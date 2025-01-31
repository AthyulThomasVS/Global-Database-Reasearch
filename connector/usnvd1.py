from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent
import mysql.connector
import json
import threading

# MySQL Settings
MYSQL_SETTINGS = {
    "host": "localhost",
    "port": 3306,  
    "user": "root",
    "passwd": "Aasath@7862",
    "database": "usnvd",  
}

events_list = []  # Store binlog events
column_cache = {}  # Cache for table column names
TIMEOUT = 20
# Set timeout in seconds

# Function to Save Events to File
def save_events_to_file():
    """Save the event list to a JSON file."""
    with open("binlog_events.json", "w") as file:
        json.dump(events_list, file, indent=4, default=str)  # Convert datetime to string

# Function to Get Column Names
def get_column_names(table_name):
    """Fetch column names for a table and cache them."""
    if table_name in column_cache:
        return column_cache[table_name]  # Return cached columns
    
    connection = mysql.connector.connect(**MYSQL_SETTINGS)
    cursor = connection.cursor()
    
    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in cursor.fetchall()]
        column_cache[table_name] = columns  # Cache column names
        return columns
    finally:
        cursor.close()
        connection.close()

# Function to Format Row Data
def format_row(table, row):
    """Format row data using actual column names."""
    columns = get_column_names(table)
    return {columns[i]: value for i, value in enumerate(row.values())} if columns else row

# Function to Stop Binlog Process
def stop_binlog(stream):
    """Stops the binlog stream after timeout."""
    print("\nTimeout reached. Stopping binlog stream...")
    stream.close()
    save_events_to_file()  # Save events before exiting
    print("Binlog stream closed and events saved.")

# Function to Process Binlog Events
def process_binlog(timeout=TIMEOUT):
    """Reads binlog events and processes them with a timeout."""
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=100,
        only_schemas=["sourcedb"],
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent],
        blocking=True,
        resume_stream=False  # Ensure fresh start
        
    )

    # Set up a timer to stop after the timeout
    timer = threading.Timer(timeout, stop_binlog, args=(stream,))
    timer.start()

    try:
        for binlog_event in stream:
            table = binlog_event.table
            for row in binlog_event.rows:
                event_data = {}

                if isinstance(binlog_event, WriteRowsEvent):
                    event_data = {
                        "operation": "INSERT",
                        "table": table,
                        "data": format_row(table, row["values"])
                    }
                elif isinstance(binlog_event, UpdateRowsEvent):
                    event_data = {
                        "operation": "UPDATE",
                        "table": table,
                        "data": format_row(table, row["after_values"])
                    }
                elif isinstance(binlog_event, DeleteRowsEvent):
                    event_data = {
                        "operation": "DELETE",
                        "table": table,
                        "data": format_row(table, row["values"])
                    }

                # Store event data
                events_list.append(event_data)
                print(event_data)  # Print for debugging

    except Exception as e:
        print(f"Error: {e}")
    finally:
        timer.cancel()  # Cancel the timer if the process stops earlier
        stream.close()  # Ensure binlog stream closes
        save_events_to_file()  # Save collected events before exiting
        print("Binlog stream closed and events saved.")

# Start Processing Binlog Events with Timeout
process_binlog()
