# Importing necessary libraries
import flask  # Flask web framework
import subprocess  # For running shell commands
import os  # For interacting with the operating system
import signal  # For sending signals to processes
import time  # For handling time-related functions

# Initializing a Flask application
app = flask.Flask(__name__)

# Defining a test endpoint
@app.route('/test')  # Corrected the decorator to use 'route'
def test_endpoint():
    return 'Test endpoint was called!'  # Response for the endpoint

def start():
    # Check if port 5000 is in use
    out = subprocess.getoutput('lsof -i:5000')  # Get the list of processes using port 5000
    if out != '':  # If there's an output, it means the port is in use
        pid = get_pid(out)  # Get the PID of the process using the port
        os.kill(pid, signal.SIGINT)  # Terminate the process gracefully
        time.sleep(1)  # Wait for a second to ensure the process has terminated

    app.run()  # Start the Flask application

def get_pid(s: str) -> int:
    # Extract the PID from the output of lsof command
    return int(list(i.split()[1] for i in s.split('\n'))[1:][0])  # Return the second line's PID

if __name__ == '__main__':
    start()  # Start the application if the script is run directly
