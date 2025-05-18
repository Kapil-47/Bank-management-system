# views/auth_view.py
class AuthView:
    @staticmethod
    def display_login():
        print("\n=== Bank System Login ===")
        user_id = input("Enter User ID (min 8 characters): ")
        password = input("Enter Password: ")
        return user_id, password

    @staticmethod
    def display_login_success(user_type, first_name):
        print(f"\nWelcome {first_name}!")
        print(f"Logged in as {user_type.capitalize()}")

    @staticmethod
    def display_login_failure():
        print("\nLogin failed. Invalid credentials or inactive account.")

    @staticmethod
    def display_logout():
        print("\nSuccessfully logged out.")



