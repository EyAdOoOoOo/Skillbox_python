# Install tabulate before running: pip install tabulate

import sqlite3
from tabulate import tabulate

DATABASE = 'hw.db'

def fetch_data(query):
    """Helper function to execute a query and fetch the results."""
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()

def format_and_print(data, headers):
    """Helper function to format and print data using the tabulate library."""
    print(tabulate(data, headers=headers, tablefmt="grid"))

def select_all_orders():
    """Fetches and displays all orders with customer and manager details."""
    query = """
        SELECT customer.full_name AS customer_name, manager.full_name AS manager_name, 
               purchase_amount, date 
        FROM "order"
        LEFT JOIN customer ON "order".customer_id = customer.customer_id
        LEFT JOIN manager ON "order".manager_id = manager.manager_id
    """
    data = fetch_data(query)
    headers = ['Customer Name', 'Manager Name', 'Purchase Amount', 'Date']
    format_and_print(data, headers)

def select_customers_without_orders():
    """Displays customers who have not made any orders."""
    query = """
        SELECT full_name 
        FROM customer
        WHERE NOT EXISTS(
            SELECT 1 
            FROM "order" 
            WHERE "order".customer_id = customer.customer_id
        )
    """
    data = fetch_data(query)
    headers = ['Customer Name']
    format_and_print(data, headers)

def select_task3():
    """Displays orders where the customer and manager are from different cities."""
    query = """
        SELECT "order".order_no, manager.full_name AS manager_name, customer.full_name AS customer_name 
        FROM "order"
        LEFT JOIN manager ON manager.manager_id = "order".manager_id
        LEFT JOIN customer ON customer.customer_id = "order".customer_id
        WHERE customer.city != manager.city
    """
    data = fetch_data(query)
    headers = ['Order No', 'Manager Name', 'Customer Name']
    format_and_print(data, headers)

def select_task4():
    """Displays orders that have no assigned manager."""
    query = """
        SELECT order_no, customer.full_name AS customer_name 
        FROM "order"
        LEFT JOIN customer ON customer.customer_id = "order".customer_id
        WHERE "order".manager_id IS NULL
    """
    data = fetch_data(query)
    headers = ['Order No', 'Customer Name']
    format_and_print(data, headers)

def main():
    # Uncomment the desired function to execute
    # select_all_orders()
    # select_customers_without_orders()
    # select_task3()
    select_task4()

if __name__ == '__main__':
    main()
