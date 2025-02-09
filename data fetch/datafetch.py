import threading
import time
from jvn import jvn
from usnvd import usnvd
from usdbinsert import usdbinsert
from jvndbinsert import jvninsert
from maindbjvninsert import maindbjvninsert
from maindbusinsert import maindbusinsert

def run_in_thread(target_function):
    thread = threading.Thread(target=target_function)
    thread.start()
    return thread

def main():
    functions = [jvn, usnvd, usdbinsert, jvninsert, maindbjvninsert, maindbusinsert]
    threads = []

    for func in functions:
        thread = run_in_thread(func)
        threads.append(thread)
        time.sleep(7)  

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
