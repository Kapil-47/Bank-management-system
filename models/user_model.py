# models/user_model.py
from sqlite3 import Error
from models.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def create_user(self, user_id, password, user_type, first_name, last_name, email, ssn_id):
        """Create a new user (employee or customer)"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            hashed_password = self.db.hash_password(password)
            cursor.execute(
                "INSERT INTO users (user_id, password, user_type, first_name, last_name, email, ssn_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, hashed_password, user_type, first_name, last_name, email, ssn_id)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            conn.close()

    def authenticate_user(self, user_id, password):
        """Authenticate user login"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            hashed_password = self.db.hash_password(password)
            cursor.execute(
                "SELECT user_id, user_type, first_name, last_name, ssn_id FROM users WHERE user_id = ? AND password = ? AND is_active = 1",
                (user_id, hashed_password)
            )
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            conn.close()

    def get_user_by_ssn(self, ssn_id):
        """Get user by SSN ID"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT user_id, first_name, last_name, email, ssn_id FROM users WHERE ssn_id = ? AND is_active = 1",
                (ssn_id,)
            )
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching user by SSN: {e}")
            return None
        finally:
            conn.close()

    def update_user(self, ssn_id, first_name, last_name, email):
        """Update user information (excluding SSN)"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET first_name = ?, last_name = ?, email = ? WHERE ssn_id = ?",
                (first_name, last_name, email, ssn_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            conn.close()

    def delete_user(self, ssn_id):
        """Mark user as inactive (soft delete)"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET is_active = 0 WHERE ssn_id = ?",
                (ssn_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()

    def get_all_active_users(self, limit=10, offset=0):
        """Get all active users with pagination"""
        conn = self.db.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT user_id, first_name, last_name, email, ssn_id FROM users WHERE is_active = 1 LIMIT ? OFFSET ?",
                (limit, offset)
            )
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching active users: {e}")
            return []
        finally:
            conn.close()