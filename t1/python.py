import datetime  # Used for handling dates and times
import random  # Provides random selections from lists
import re  # Allows us to use regular expressions for text analysis

# Importing the Flask class to create our web app
from flask import Flask

# Initialize a new Flask application
app = Flask(__name__)

# A list of popular car brands
cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']

# A list of cat breeds (in Russian)
cats_list = ['Корниш-рекс', 'Русская голубая', 'Шотландская вислоухая', 'Мейн-кун', 'Манчкин']

# Read the text of War and Peace (in Russian) from a file
war_and_peace = open('static/war_and_peace.txt', 'r', encoding='UTF-8').read()

# This variable tracks how many times the /counter route has been accessed
visits = 0

# Define a route for the URL /hello_world that returns a simple greeting
@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'  # Returns a greeting in Russian, meaning "Hello, world!"

# Define a route for the URL /cars that lists available car brands
@app.route('/cars')
def cars():
    global cars_list
    return ' '.join(cars_list)  # Returns the list of car brands, separated by spaces

# Define a route for /cats that selects a random cat breed from the list
@app.route('/cats')
def cats():
    return random.choice(cats_list)  # Returns one random cat breed from the list

# Define a route for /get_time/now to display the current time
@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.datetime.now()
    return f'Точное время: {current_time}'  # Displays the current time in Russian

# Define a route for /get_time/future to show the time one hour from now
@app.route('/get_time/future')
def get_time_future():
    current_time = datetime.datetime.now()
    future_time = current_time + datetime.timedelta(hours=1)
    return f'Точное время через час будет: {future_time}'  # Shows the time an hour later

# Function to extract words from War and Peace using regular expressions
def get_word_list():
    return re.findall(r'[a-zA-Zа-яА-Я]+', war_and_peace)

# Define a route for /get_random_word that returns a random word from War and Peace
@app.route('/get_random_word')
def get_random_word():
    return random.choice(get_word_list())  # Picks a random word from the text

# Define a route for /counter that tracks how many times the page has been visited
@app.route('/counter')
def counter():
    global visits
    visits += 1  # Increments the visit counter each time this route is accessed
    return str(visits)  # Returns the current count of visits

# If this script is executed directly, start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)  # Runs the app in debug mode for easier error tracing

