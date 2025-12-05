import sqlite3
import shutil
import os
from datetime import datetime

DB_NAME = "pos_data.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    conn = connect()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        pin TEXT,
        role TEXT
    )
    """)

    # Settings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        shop_name TEXT,
        owner_name TEXT,
        address TEXT,
        phone TEXT,
        logo_path TEXT,
        theme TEXT
    )
    """)

    cur.execute("INSERT OR IGNORE INTO settings (id, theme) VALUES (1, 'light')")

    # Services
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        name TEXT,
        unit TEXT,
        price REAL
    )
    """)

    # Payment Methods
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        method TEXT
    )
    """)

    # Bills (header)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_no TEXT UNIQUE,
        customer_name TEXT,
        payment_method TEXT,
        date TEXT,
        time TEXT,
        total REAL,
        user_id INTEGER
    )
    """)

    # Items inside a bill
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        service_id INTEGER,
        service_name TEXT,
        unit_price REAL,
        quantity REAL,
        subtotal REAL
    )
    """)

    # Expenses
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        notes TEXT
    )
    """)

    # Credit Customers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS credit_customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        phone TEXT,
        total_due REAL
    )
    """)

    # Ledger
    cur.execute("""
    CREATE TABLE IF NOT EXISTS credit_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        date TEXT,
        amount REAL,
        type TEXT,
        notes TEXT
    )
    """)

    # Counters
    cur.execute("""
    CREATE TABLE IF NOT EXISTS counters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        print_pages INTEGER,
        xerox_pages INTEGER,
        scans INTEGER
    )
    """)

    conn.commit()
    conn.close()

    # Auto backup daily
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d')}.db"
    if not os.path.exists(backup_name):
        shutil.copy(DB_NAME, backup_name)
