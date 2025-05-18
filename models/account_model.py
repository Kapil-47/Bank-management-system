# models/account_model.py
from sqlite3 import Error
from models.database import Database

class AccountModel:
    def __init__(self):
        self.db = Database()

    def create_account(self, customer_ssn_id, account_type):
        """Create a new bank account"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO accounts (customer_ssn_id, account_type) VALUES (?, ?)",
                (customer_ssn_id, account_type)
            )
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error creating account: {e}")
            return None
        finally:
            conn.close()

    def get_accounts_by_ssn(self, customer_ssn_id):
        """Get all accounts for a customer"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT account_id, account_type, balance FROM accounts WHERE customer_ssn_id = ? AND is_active = 1",
                (customer_ssn_id,)
            )
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching accounts: {e}")
            return []
        finally:
            conn.close()

    def get_account_balance(self, account_id):
        """Get current balance of an account"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_id = ? AND is_active = 1",
                (account_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Error getting account balance: {e}")
            return None
        finally:
            conn.close()

    def update_balance(self, account_id, amount):
        """Update account balance"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
                (amount, account_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating balance: {e}")
            return False
        finally:
            conn.close()

    def transfer_amount(self, from_account_id, to_account_id, amount):
        """Transfer amount between accounts"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Check if from account has sufficient balance
            from_balance = self.get_account_balance(from_account_id)
            if from_balance is None or from_balance < amount:
                raise ValueError("Insufficient balance")
            
            # Deduct from source account
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE account_id = ?",
                (amount, from_account_id)
            )
            
            # Add to destination account
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
                (amount, to_account_id)
            )
            
            # Record transactions
            self._record_transaction(cursor, from_account_id, -amount, 'transfer', f"Transfer to account {to_account_id}")
            self._record_transaction(cursor, to_account_id, amount, 'transfer', f"Transfer from account {from_account_id}")
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error during transfer: {e}")
            return False
        finally:
            conn.close()

    def _record_transaction(self, cursor, account_id, amount, transaction_type, description):
        """Helper method to record a transaction"""
        cursor.execute(
            "INSERT INTO transactions (account_id, amount, transaction_type, description) VALUES (?, ?, ?, ?)",
            (account_id, abs(amount), transaction_type, description)
        )