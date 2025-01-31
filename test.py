import threading
import time
import asyncio
from database_handler.binlog_processor import process_binlog
from database_handler.data_extraction import extract_and_store
#from database_handler.translate import translate_descriptions  #

def run_binlog():
    print("Starting binlog processing...")
    process_binlog()
    print("Binlog processing completed.")

def run_extraction():
    print("Extracting and storing data...")
    extract_and_store()
    print("Data extraction completed.")

#async def run_translation():
#    print("Translating descriptions...")
#    await translate_descriptions()  
#    print("Translation completed.")

def main():
    binlog_thread = threading.Thread(target=run_binlog)
    extraction_thread = threading.Thread(target=run_extraction)

    binlog_thread.start()
    time.sleep(30)  
    extraction_thread.start()
    time.sleep(30) 
   #asyncio.run(run_translation())

    binlog_thread.join()
    extraction_thread.join()

    print("All processes completed.")

if __name__ == "__main__":
    main()
