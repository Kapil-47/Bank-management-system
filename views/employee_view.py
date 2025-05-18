# views/employee_view.py
class EmployeeView:
    @staticmethod
    def display_menu():
        print("\n=== Employee Menu ===")
        print("1. Create New Account Holder")
        print("2. Edit Account Holder Information")
        print("3. Delete Account Holder")
        print("4. View All Active Account Holders")
        print("5. Search Account Holder")
        print("6. Logout")
        return input("Enter your choice (1-6): ")

    @staticmethod
    def display_create_account_holder():
        print("\n=== Create New Account Holder ===")
        user_id = input("Enter User ID (min 8 alphanumeric characters): ")
        password = input("Enter Password (10 chars with special, upper, number): ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        ssn_id = input("SSN ID (9 digits): ")
        account_type = input("Account Type (checking/savings): ")
        return {
            'user_id': user_id,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'ssn_id': ssn_id,
            'account_type': account_type
        }

    @staticmethod
    def display_edit_account_holder():
        print("\n=== Edit Account Holder ===")
        ssn_id = input("Enter SSN ID of account holder to edit: ")
        first_name = input("New First Name (leave blank to keep current): ")
        last_name = input("New Last Name (leave blank to keep current): ")
        email = input("New Email (leave blank to keep current): ")
        return {
            'ssn_id': ssn_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

    @staticmethod
    def display_delete_account_holder():
        print("\n=== Delete Account Holder ===")
        return input("Enter SSN ID of account holder to delete: ")

    @staticmethod
    def display_search_account_holder():
        print("\n=== Search Account Holder ===")
        return input("Enter SSN ID to search: ")

    @staticmethod
    def display_account_holder_info(user_info, accounts):
        print("\n=== Account Holder Information ===")
        if not user_info:
            print("No account holder found with that SSN ID.")
            return
        
        user_id, first_name, last_name, email, ssn_id = user_info
        print(f"\nName: {first_name} {last_name}")
        print(f"Email: {email}")
        print(f"SSN ID: {ssn_id}")
        print(f"User ID: {user_id}")
        
        if accounts:
            print("\nAccounts:")
            for account in accounts:
                account_id, account_type, balance = account
                print(f"  Account ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

    @staticmethod
    def display_all_account_holders(users, page, total_pages):
        print(f"\n=== Active Account Holders (Page {page} of {total_pages}) ===")
        if not users:
            print("No active account holders found.")
            return
        
        for user in users:
            user_id, first_name, last_name, email, ssn_id = user
            print(f"\nName: {first_name} {last_name}")
            print(f"Email: {email}")
            print(f"SSN ID: {ssn_id}")
            print(f"User ID: {user_id}")
            print("-" * 30)

    @staticmethod
    def display_operation_result(success, operation):
        if success:
            print(f"\n{operation} completed successfully!")
        else:
            print(f"\n{operation} failed. Please try again.")

    @staticmethod
    def display_pagination_options(page, total_pages):
        print("\nNavigation:")
        if page > 1:
            print("P - Previous Page")
        if page < total_pages:
            print("N - Next Page")
        print("M - Return to Menu")
        return input("Enter choice: ").upper()
