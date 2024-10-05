import requests
from flask import Flask, render_template, request
from datetime import datetime
import sys, os

# Initialize a Flask web application
app = Flask(__name__)

# Task 1: Function to sum values from a file
def get_summary_rss(path):
    # Open the file at the given path and read its lines (ignoring the first line)
    lines = open(path, 'r', encoding='UTF-8').readlines()[1:]
    sum = 0
    # Loop through each line and sum the sixth column values (assuming it's an integer)
    for line in lines:
        sum += int(line.split()[5])

    # Return the total sum
    return sum


# Task 2: Function to convert bytes to a human-readable format
def convert_measure(bytes):
    # Convert the byte value to float
    res = float(bytes)
    cnt = 0
    # Define the unit names for the conversion
    names = ['B', 'KB', 'MB', 'GB', 'TB']
    # Loop until the value is less than 1024, dividing by 1024 each time
    while res > 1024:
        res /= 1024
        cnt += 1

    # Return the result formatted with three decimal places and the appropriate unit
    return f'{res:.3f} {names[cnt]}'

# Function to calculate the mean size from the input data
def get_mean_size():
    # Read lines from standard input, skipping the first line
    data = sys.stdin.readlines()[1:]

    sum = 0
    cnt = 0
    # Loop through each line and sum the 5th column values
    for line in data:
        sum += float(line.split()[4])
        cnt += 1
    # If no data, return 0
    if cnt <= 0:
        return 0
    # Return the mean size
    return sum / cnt
    return data

# Task 3: Function to decrypt a given code
def decrypt(code):
    decrypted_str = ''
    temp = code.strip()  # Remove any surrounding whitespace
    i = 0
    # Loop while there are '.' characters in the string
    while temp.count('.') > 0:
        if temp[i] == '.':
            # If the last character is '.', clear the string and exit
            if i == len(temp) - 1:
                temp = ''
                break
            # Skip to the next character after '.'
            temp = temp[i + 1:]
            continue
        # Stop if less than 3 characters remain
        if i > len(temp) - 3:
            break
        # Skip spaces
        if temp[i].isspace():
            continue
        # Handle different cases of '.' sequences
        if temp[i] != '.':
            if temp[i + 1] == '.':
                if temp[i + 2] == '.':
                    if i > 0:
                        temp = temp[: i] + temp[i + 2:]
                        i -= 1
                        continue
                    else:
                        temp = temp[i + 3:]
                        continue
                else:
                    temp = temp[:i + 1] + temp[i + 2:]
                    i += 1
                    continue
            else:
                i += 1
                continue

    decrypted_str = temp  # Store the remaining string
    return decrypted_str  # Return the decrypted string

# Route to handle the homepage
@app.route('/')
def index():
    # Path to the file being processed
    path = '/home/andrew/Projects/advancedPython/PythonProg2/mod2/output_file.txt'
    context = {}
    # Task 1: Get the memory usage and format it
    context['task1'] = f'Объем потребляемой памяти: {convert_measure(get_summary_rss(path))}'
    # Task 3: Decrypt the message from stdin and add it to the context
    context['task3'] = f'\nРасшифрованное сообщение: {decrypt(sys.stdin.read())}'
    context['task4'] = ''
    # Render the 'index.html' template with the context
    return render_template('index.html', context=context)

# Dictionary for day-related messages
days = {
    0 : ['его', 'понедельника'],
    1 : ['его', 'вторника'],
    2 : ['ей', 'среды'],
    3 : ['его', 'четверга'],
    4 : ['ей', 'пятницы'],
    5 : ['ей', 'субботы'],
    6 : ['его', 'воскресенья'],
}

# Task 4: Route to display a greeting message with the current day of the week
@app.route('/hello-world/<name>')
def hello_world(name):
    # Get the current weekday as an integer (0=Monday, 6=Sunday)
    day = datetime.today().weekday()
    # Return a greeting message that includes the current day of the week
    return f'Привет ,{name}. Хорош{days[day][0]} {days[day][1]} !'

# Task 5: Route to find and display the maximum number from a list of numbers in the URL
@app.route('/max_number/<path:num>')
def max_number(num):
    # Split the URL path into numbers, filter out non-digit characters, and convert them to integers
    nums = list(int(i) for i in num.split('/') if i.isdigit() or i == '-')
    # Return the largest number from the list
    return f'Наибольшее число: {sorted(nums)[-1]}'

# Task 6: Route to preview a file with a specified size limit
@app.route('/file-preview/<int:SIZE>/<path:RELATIVE_PATH>')
def file_preview(SIZE, RELATIVE_PATH):
    # Get the absolute file path from the relative path
    abs_path = os.path.abspath(RELATIVE_PATH)
    # Read the first SIZE characters from the file
    preview = open(abs_path, 'r').read(SIZE)
    # Return the absolute file path, the size of the preview, and the preview text
    return f'<abs_path>{abs_path}</abs_path> <result_size>{len(preview)}</result_size><br><result_text>{preview}</result_text>'

# Storage dictionary for storing date and number pairs
storage = {}

# Route to add and store a number for a specific date
@app.route('/add/<date>/<int:number>', methods=['POST', 'GET'])
def save_date(date, number):
    # Convert the date from ISO format to a datetime object
    date = datetime.fromisoformat(date)
    # Store the number under the correct year, month, and day in the storage dictionary
    storage.setdefault(date.year, {}).setdefault(date.month, {}).setdefault(date.day, {})
    storage[date.year][date.month][date.day] = number
    return ''

# Route to calculate and display the total sum for a specific year
@app.route('/calculate/<int:year>')
def calculate_year(year):
    # If the year isn't in storage, initialize an empty dictionary for it
    if year not in storage:
        storage[year] = {}
    sum = 0
    # Sum all values stored under the year
    for k1, v1 in storage[year].items():
        for k2, v2 in v1.items():
            sum += v2

    # Return the total sum for the year
    return f'Сумма за {year} год: {sum} руб.'

# Dictionary for month names in Russian
months = {
    1: 'январь',
    2: 'февраль',
    3: 'март',
    4: 'апрель',
    5: 'май',
    6: 'июнь',
    7: 'июль',
    8: 'август',
    9: 'сентябрь',
    10: 'октябрь',
    11: 'ноябрь',
    12: 'декабрь',
}

# Route to calculate and display the total sum for a specific month of a year
@app.route('/calculate/<int:year>/<int:month>')
def calculate_year_month(year, month):
    # If the year isn't in storage, initialize it
    if year not in storage:
        storage[year] = {}
    # If the month isn't in storage for that year, initialize it
    if month not in storage[year]:
        storage[year][month] = {}
    sum = 0
    # Sum all values stored under the specific month of the year
    for k, v in storage[year][month].items():
        sum += v

    # Return the total sum for the month
    return f'Сумма за {months[month]} месяц {year} года: {sum} руб.'

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
