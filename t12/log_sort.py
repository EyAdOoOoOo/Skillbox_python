import threading
from threading import Semaphore
import time
from datetime import datetime, timedelta
import requests
import logging

# Base URL for fetching timestamps
URL = 'http://127.0.0.1:5000/timestamp/'

# Semaphore object for thread synchronization
sem = Semaphore()

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=f'{__name__}.log', filemode='w')

# Flag to stop logging after a certain time
STOP_LOGGING = False

def log_data():
    """
    Function to log timestamp data every second for 20 seconds.
    Each thread will fetch the current timestamp and the corresponding date from the URL.
    """
    start_time = datetime.now()

    # Run the loop for 20 seconds
    while (datetime.now() - start_time) < timedelta(seconds=20):
        with sem:  # Ensure only one thread logs data at a time
            timestamp = datetime.timestamp(datetime.now())
            response = requests.get(f"{URL}{timestamp}")  # Fetch the date corresponding to the timestamp
            logger.info(f'Timestamp: {timestamp:.3f}\t\tDate: {response.text}')  # Log the result

        time.sleep(1)  # Wait for 1 second before the next request

def main():
    """
    Main function to start 10 threads, each logging data from the log_data function.
    Threads start with a 1-second interval between them.
    """
    # Create 10 threads, each running the log_data function
    threads = [threading.Thread(target=log_data) for _ in range(10)]

    # Start each thread with a delay of 1 second
    for thread in threads:
        thread.start()
        time.sleep(1)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
