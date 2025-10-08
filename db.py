import sqlite3

def get_connection():
    conn = sqlite3.connect("data/expenses.db", check_same_thread=False)
    return conn

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

def add_expense(amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                   (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = get_connection()
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def update_expense(expense_id, amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses 
        SET amount=?, category=?, description=?, date=? 
        WHERE id=?""",
        (amount, category, description, date, expense_id)
    )
    conn.commit()
    conn.close()
