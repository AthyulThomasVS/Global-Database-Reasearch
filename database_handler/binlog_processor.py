import json
import threading
import mysql.connector
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent

MYSQL_SETTINGS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "Aasath@7862",
    "database": "usnvd",
}

events_list = []
column_cache = {}
TIMEOUT = 4
stop_event = threading.Event()  # Stop flag

def save_events_to_file():
    with open("binlog_events.json", "w") as file:
        json.dump(events_list, file, indent=4, default=str)

def get_column_names(table_name):
    if table_name in column_cache:
        return column_cache[table_name]
    connection = mysql.connector.connect(**MYSQL_SETTINGS)
    cursor = connection.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    column_cache[table_name] = columns
    cursor.close()
    connection.close()
    return columns

def format_row(table, row):
    columns = get_column_names(table)
    return {columns[i]: value for i, value in enumerate(row.values())} if columns else row

def stop_binlog(stream):
    print("\nTimeout reached. Stopping binlog stream...")
    stop_event.set()  # Set stop flag
    stream.close()
    save_events_to_file()
    print("Binlog stream closed and events saved.")

def process_binlog(timeout=TIMEOUT):
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=100,
        only_schemas=["sourcedb"],
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent],
        blocking=True,
        resume_stream=False
    )

    timer = threading.Timer(timeout, stop_binlog, args=(stream,))
    timer.start()

    try:
        for binlog_event in stream:
            if stop_event.is_set():  # Stop processing if timeout reached
                break

            table = binlog_event.table
            for row in binlog_event.rows:
                event_data = {}
                if isinstance(binlog_event, WriteRowsEvent):
                    event_data = {"operation": "INSERT", "table": table, "data": format_row(table, row["values"])}
                elif isinstance(binlog_event, UpdateRowsEvent):
                    event_data = {"operation": "UPDATE", "table": table, "data": format_row(table, row["after_values"])}
                elif isinstance(binlog_event, DeleteRowsEvent):
                    event_data = {"operation": "DELETE", "table": table, "data": format_row(table, row["values"])}
                
                events_list.append(event_data)
                print(event_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        timer.cancel()
        stream.close()
        save_events_to_file()
        print("Binlog stream closed and events saved.")
        exit()

    
