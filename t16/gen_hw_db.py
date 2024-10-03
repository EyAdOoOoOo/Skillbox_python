import random
import sqlite3

# SQL commands to create tables for 'customer', 'manager', and 'order'
CREATE_TABLES = """
DROP TABLE IF EXISTS 'customer';
CREATE TABLE 'customer' (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    manager_id INTEGER REFERENCES manager(manager_id)
);

DROP TABLE IF EXISTS 'manager';
CREATE TABLE 'manager' (
    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS 'order';
CREATE TABLE 'order' (
    order_no INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_amount INTEGER NOT NULL,
    date VARCHAR(255) NOT NULL,
    customer_id INTEGER REFERENCES customer(customer_id),
    manager_id INTEGER REFERENCES manager(manager_id)
);
"""

# Function to generate random dates
def _get_random_date() -> str:
    day = random.randint(1, 30)
    month = random.randint(1, 12)
    return f"2020-{month}-{day}"

# Predefined list of Russian family names
families = """Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв""".split()

# Letters for generating random initials
name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()

# Function to generate random full names
def _get_random_full_name() -> str:
    is_male = random.choice((True, False))
    family_name = random.choice(families)
    
    if not is_male:
        family_name += "а"  # Append 'а' for female names
    
    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)
    return f"{family_name} {first_letter}.{last_letter}."

# List of cities for random selection
cities = """
Москва
Омск
Барнаул
Ярославль
Краснодар
Севастополь
Ялта
Сочи
Ижевск
Иркутск
Мурманск
Санкт-Петербург
Архангельск
""".split()

# Function to create and populate tables
def prepare_tables():
    if __name__ == "__main__":
        # Establish a connection to the database
        with sqlite3.connect("hw.db") as conn:
            cursor = conn.cursor()
            # Create tables
            cursor.executescript(CREATE_TABLES)
            conn.commit()
            
            # Insert random managers into 'manager' table
            managers = [
                (_get_random_full_name(), random.choice(cities)) 
                for _ in range(30)
            ]
            conn.executemany("""
                INSERT INTO 'manager'(full_name, city) 
                VALUES (?, ?)
            """, managers)

            # Insert random customers into 'customer' table
            customers = [
                (
                    _get_random_full_name(),
                    random.choice(cities),
                    random.choice([i for i in range(1, 21)] + [None])
                ) 
                for _ in range(500)
            ]
            conn.executemany("""
                INSERT INTO 'customer'(full_name, city, manager_id) 
                VALUES(?, ?, ?)
            """, customers)

            # Insert random orders into 'order' table
            orders = [
                (
                    random.randint(10, 1000),  # purchase amount
                    _get_random_date(),        # random date
                    random.randint(1, 100),    # random customer_id
                    random.choice([i for i in range(1, 21)] + [None])  # manager_id or None
                ) 
                for _ in range(10000)
            ]
            conn.executemany("""
                INSERT INTO 'order'(purchase_amount, date, customer_id, manager_id) 
                VALUES(?, ?, ?, ?)
            """, orders)

# Run the function to set up the tables and data
if __name__ == '__main__':
    prepare_tables()
