from multiprocessing.pool import ThreadPool, Pool
import datetime
import sqlite3
import threading
import requests

# Base URL for API requests and database name
BASE_URL = 'https://www.swapi.tech/api/people/'
DATABASE = 'sqlite3.db'

# Initialize the SQLite database
def init_db():
    """
    Initializes the database by creating the 'People' table if it doesn't exist.
    If the table exists, its contents are deleted.
    """
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        try:
            # Clear the table if it exists
            cur.execute('DELETE FROM People')
            con.commit()
        except sqlite3.OperationalError:
            # Create the table if it doesn't exist
            cur.execute('''
                CREATE TABLE People (
                    id INTEGER PRIMARY KEY, 
                    name VARCHAR(255), 
                    gender VARCHAR(255), 
                    birth_year VARCHAR(255)
                )
            ''')

# Lock object for thread safety when writing to the database
lock = threading.Lock()

def get_and_add_person_by_request(i):
    """
    Makes a GET request to the API for a person, retrieves their data, 
    and inserts it into the SQLite database.
    """
    # Request data from the API
    response = requests.get(BASE_URL + str(i))
    data = response.json()

    # Extract properties if available
    if 'result' in data and 'properties' in data['result']:
        data = data['result']['properties']

    # Insert the data into the database, ensuring thread safety with a lock
    with lock:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            if 'name' in data:
                cur.execute(
                    'INSERT INTO People VALUES (?, ?, ?, ?)', 
                    (i, data["name"], data["gender"], data["birth_year"])
                )
                con.commit()

def pool_adding():
    """
    Adds people using a Pool of processes for parallel API requests.
    """
    print('Pool started!')
    start = datetime.datetime.now()

    # Use multiprocessing Pool to make requests in parallel
    with Pool(processes=20) as pool:
        pool.map(get_and_add_person_by_request, range(1, 21))

    print(f'Pool time: {datetime.datetime.now() - start}')

def thread_pool_adding():
    """
    Adds people using a ThreadPool for parallel API requests.
    """
    print('Thread pool started!')
    start = datetime.datetime.now()

    # Use ThreadPool to make requests in parallel
    with ThreadPool(processes=20) as thread_pool:
        thread_pool.map(get_and_add_person_by_request, range(1, 21))

    print(f'Thread pool time: {datetime.datetime.now() - start}')

def main():
    """
    Main function that initializes the database and runs both the thread pool 
    and process pool methods for comparison.
    """
    init_db()  # Initialize the database (clear or create table)
    thread_pool_adding()  # Run the ThreadPool version
    init_db()  # Re-initialize the database to start fresh
    pool_adding()  # Run the Pool (multiprocessing) version

if __name__ == '__main__':
    main()
