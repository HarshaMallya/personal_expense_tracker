import sqlite3
import os
import pandas as pd

# ✅ Step 1: Safely create or connect to the database
def get_connection():
    # Ensure the 'data' directory exists before connecting
    os.makedirs("data", exist_ok=True)

    # Create a proper path for Streamlit Cloud (safe and flexible)
    db_path = os.path.join("data", "expenses.db")

    # Connect to the database
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn


# ✅ Step 2: Create table if not exists
def create_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()


# ✅ Step 3: Add a new expense
def add_expense(amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))
    conn.commit()
    conn.close()


# ✅ Step 4: Fetch all expenses
def get_expenses():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df


# ✅ Step 5: Delete an expense
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()


# ✅ Step 6: Update an existing expense
def update_expense(expense_id, amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses 
        SET amount=?, category=?, description=?, date=? 
        WHERE id=?
    """, (amount, category, description, date, expense_id))
    conn.commit()
    conn.close()
