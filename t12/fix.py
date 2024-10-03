from threading import Semaphore, Thread
import time

# Create a Semaphore object for thread synchronization
sem = Semaphore()

# Flag to stop the threads when needed
stop_thread = False

def print_1():
    global stop_thread
    while not stop_thread:
        with sem:
            print(1)
        time.sleep(0.25)  # Pause for 0.25 seconds

def print_2():
    global stop_thread
    while not stop_thread:
        with sem:
            print(2)
        time.sleep(0.25)  # Pause for 0.25 seconds

# Create threads that target the print_1 and print_2 functions
thread_1 = Thread(target=print_1)
thread_2 = Thread(target=print_2)

try:
    thread_1.start()  # Start thread 1
    thread_2.start()  # Start thread 2

    # Run an infinite loop until interrupted by the user (Ctrl+C)
    while True:
        pass  # Keep the main thread alive

except KeyboardInterrupt:
    # Handle Ctrl+C (keyboard interrupt) and stop the threads
    print('\nReceived keyboard interrupt, stopping threads...')
    stop_thread = True  # Set the flag to stop both threads
    thread_1.join()  # Wait for thread 1 to finish
    print('Thread 1 stopped!')
    thread_2.join()  # Wait for thread 2 to finish
    print('Thread 2 stopped!')
