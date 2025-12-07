import sqlite3
import os

db_path = 'users.db'

if not os.path.exists(db_path):
    print(f"Database {db_path} not found.")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_table(table_name):
    print(f"\n--- Table: {table_name} ---")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            print("(Empty)")
            return

        # Calculate column widths
        widths = [len(c) for c in columns]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        
        # Print header
        header = " | ".join(f"{col:<{w}}" for col, w in zip(columns, widths))
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in rows:
            print(" | ".join(f"{str(val):<{w}}" for val, w in zip(row, widths)))
            
    except sqlite3.OperationalError as e:
        print(f"Error reading table {table_name}: {e}")

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    print_table(table[0])

conn.close()

