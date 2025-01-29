from mysqlreplication.binlog import BinLogStreamReader
from mysqlreplication.rowevents import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent
import mysql.connector
import logging
import time

# Set up logging
logging.basicConfig(filename='cdc_monitor.log', level=logging.INFO)

# Function to process binlog events
def process_event(event):
    if isinstance(event, WriteRowsEvent):
        logging.info(f"INSERT: {event.rows}")
    elif isinstance(event, UpdateRowsEvent):
        logging.info(f"UPDATE: {event.rows}")
    elif isinstance(event, DeleteRowsEvent):
        logging.info(f"DELETE: {event.rows}")

# Set up connection to MySQL
def start_cdc():
    connection = mysql.connector.connect(
        host='your_mysql_host',
        user='cdc_user',
        password='your_password',
        database='your_database'
    )

    # Set up the BinLog stream reader
    stream = BinLogStreamReader(connection_settings={
        'host': 'your_mysql_host',
        'port': 3306,
        'user': 'cdc_user',
        'passwd': 'your_password'
    }, blocking=True, resume_stream=True)

    logging.info("Starting CDC Monitoring...")

    try:
        for event in stream:
            process_event(event)

    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        stream.close()

# Continuously monitor
if __name__ == "__main__":
    while True:
        try:
            start_cdc()
        except Exception as e:
            logging.error(f"Error restarting CDC: {e}")
        logging.info("Restarting CDC in 10 seconds...")
        time.sleep(10)  # Sleep before restarting if it crashes
