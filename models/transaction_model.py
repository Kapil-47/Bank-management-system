# models/transaction_model.py
from sqlite3 import Error
from models.database import Database

class TransactionModel:
    def __init__(self):
        self.db = Database()

    def get_transactions(self, account_id, limit=10, offset=0):
        """Get transaction history for an account"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """SELECT strftime('%Y-%m-%d %H:%M:%S', created_at) as date, 
                       amount, transaction_type, description 
                FROM transactions 
                WHERE account_id = ? 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?""",
                (account_id, limit, offset)
            )
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching transactions: {e}")
            return []
        finally:
            conn.close()

    def deposit(self, account_id, amount, description="Deposit"):
        """Record a deposit transaction"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            # Update account balance
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
                (amount, account_id)
            )
            
            # Record transaction
            cursor.execute(
                "INSERT INTO transactions (account_id, amount, transaction_type, description) VALUES (?, ?, ?, ?)",
                (account_id, amount, 'credit', description)
            )
            
            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print(f"Error during deposit: {e}")
            return False
        finally:
            conn.close()

    def withdraw(self, account_id, amount, description="Withdrawal"):
        """Record a withdrawal transaction"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            # Check balance first
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_id = ?",
                (account_id,)
            )
            balance = cursor.fetchone()[0]
            
            if balance < amount:
                raise ValueError("Insufficient balance")
            
            # Update account balance
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE account_id = ?",
                (amount, account_id)
            )
            
            # Record transaction
            cursor.execute(
                "INSERT INTO transactions (account_id, amount, transaction_type, description) VALUES (?, ?, ?, ?)",
                (account_id, amount, 'debit', description)
            )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error during withdrawal: {e}")
            return False
        finally:
            conn.close()