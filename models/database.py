# models/database.py
import sqlite3
from sqlite3 import Error
import hashlib

class Database:
    def __init__(self, db_file="bank_system.db"):
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        """Create a database connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute("PRAGMA foreign_keys = ON")
            return self.conn
        except Error as e:
            print(e)
        return None

    def initialize_database(self):
        """Initialize database tables"""
        sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK(user_type IN ('employee', 'customer')),
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            ssn_id TEXT UNIQUE NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        sql_create_accounts_table = """
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_ssn_id TEXT NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (customer_ssn_id) REFERENCES users (ssn_id) ON DELETE CASCADE
        );
        """

        sql_create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('credit', 'debit', 'transfer')),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE
        );
        """

        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute(sql_create_users_table)
            cursor.execute(sql_create_accounts_table)
            cursor.execute(sql_create_transactions_table)
            conn.commit()
            
            # Create a default admin employee if not exists
            admin_id = "admin1234"
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (admin_id,))
            if not cursor.fetchone():
                hashed_password = hashlib.sha256("Admin@1234".encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO users (user_id, password, user_type, first_name, last_name, email, ssn_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (admin_id, hashed_password, 'employee', 'Admin', 'User', 'admin@bank.com', '123456789')
                )
                conn.commit()
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()