from flask import Flask
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Enable debug mode for easier troubleshooting
app.config['DEBUG'] = True

@app.route('/timestamp/<stamp>')
def timestamp(stamp):
    """
    Converts a timestamp from the URL parameter into a human-readable datetime format.
    """
    # Convert the timestamp to a float, then convert it to a datetime object
    return f'{datetime.fromtimestamp(float(stamp))}'

def main():
    """
    Main function to run the Flask app.
    """
    app.run()

# Run the main function when the script is executed
if __name__ == '__main__':
    main()
