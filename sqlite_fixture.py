import sqlite3
from datetime import datetime, timedelta
import random

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()

    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount DECIMAL(10,2) NOT NULL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
    ''')

    # Create comments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
    ''')

    # Sample customer data
    customers = [
        ('John Doe', 'john.doe@email.com', '+1234567890'),
        ('Jane Smith', 'jane.smith@email.com', '+1987654321'),
        ('Bob Johnson', 'bob.johnson@email.com', '+1122334455'),
        ('Alice Brown', 'alice.brown@email.com', '+1555666777'),
        ('Charlie Wilson', 'charlie.wilson@email.com', '+1888999000'),
        ('Diana Miller', 'diana.miller@email.com', '+1777888999'),
        ('Edward Davis', 'edward.davis@email.com', '+1666777888'),
        ('Fiona Clark', 'fiona.clark@email.com', '+1555666777'),
        ('George White', 'george.white@email.com', '+1444555666'),
        ('Hannah Lee', 'hannah.lee@email.com', '+1333444555')
    ]

    # Insert customer data
    cursor.executemany('''
    INSERT INTO customers (name, email, mobile)
    VALUES (?, ?, ?)
    ''', customers)

    # Sample sales data
    sales = []
    for customer_id in range(1, 11):  # For each customer
        # Generate 1-3 sales per customer
        for _ in range(random.randint(1, 3)):
            amount = round(random.uniform(10.0, 1000.0), 2)
            sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
            sales.append((customer_id, amount, sale_date))

    # Insert sales data
    cursor.executemany('''
    INSERT INTO sales (customer_id, amount, sale_date)
    VALUES (?, ?, ?)
    ''', sales)

    # Sample comments data
    comments = [
        (1, "Great service! Will come back again."),
        (1, "Product quality is excellent."),
        (2, "Very satisfied with the purchase."),
        (3, "Fast delivery and good packaging."),
        (4, "Customer service was helpful."),
        (5, "Prices are reasonable."),
        (6, "Good selection of products."),
        (7, "Website is easy to navigate."),
        (8, "Quick response to queries."),
        (9, "Overall good experience."),
        (10, "Would recommend to others.")
    ]

    # Insert comments data
    cursor.executemany('''
    INSERT INTO comments (customer_id, comment)
    VALUES (?, ?)
    ''', comments)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def print_sample_data():
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()

    # Print customers
    print("\n=== Customers ===")
    cursor.execute('SELECT * FROM customers')
    for row in cursor.fetchall():
        print(row)

    # Print sales
    print("\n=== Sales ===")
    cursor.execute('SELECT * FROM sales')
    for row in cursor.fetchall():
        print(row)

    # Print comments
    print("\n=== Comments ===")
    cursor.execute('SELECT * FROM comments')
    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    create_database()
    print_sample_data()
