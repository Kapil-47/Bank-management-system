# views/customer_view.py
class CustomerView:
    @staticmethod
    def display_menu():
        print("\n=== Customer Menu ===")
        print("1. View Account Details")
        print("2. View Transaction History")
        print("3. Transfer Amount")
        print("4. Edit Profile")
        print("5. Logout")
        return input("Enter your choice (1-5): ")

    @staticmethod
    def display_account_details(accounts):
        print("\n=== Your Accounts ===")
        if not accounts:
            print("No active accounts found.")
            return
        
        for account in accounts:
            account_id, account_type, balance = account
            print(f"\nAccount ID: {account_id}")
            print(f"Type: {account_type}")
            print(f"Balance: ${balance:.2f}")

    @staticmethod
    def display_transaction_history(transactions):
        print("\n=== Transaction History ===")
        if not transactions:
            print("No transactions found.")
            return
        
        for transaction in transactions:
            date, amount, trans_type, description = transaction
            print(f"\nDate: {date}")
            print(f"Type: {trans_type.capitalize()}")
            print(f"Amount: ${amount:.2f}")
            print(f"Description: {description}")
            print("-" * 30)

    @staticmethod
    def display_transfer_amount():
        print("\n=== Transfer Amount ===")
        from_account = input("Enter your account ID to transfer from: ")
        to_account = input("Enter destination account ID: ")
        amount = input("Enter amount to transfer: ")
        return from_account, to_account, amount

    @staticmethod
    def display_edit_profile(current_info):
        print("\n=== Edit Profile ===")
        print(f"Current First Name: {current_info[0]}")
        first_name = input("New First Name (leave blank to keep current): ")
        print(f"\nCurrent Last Name: {current_info[1]}")
        last_name = input("New Last Name (leave blank to keep current): ")
        print(f"\nCurrent Email: {current_info[2]}")
        email = input("New Email (leave blank to keep current): ")
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

    @staticmethod
    def display_operation_result(success, operation):
        if success:
            print(f"\n{operation} completed successfully!")
        else:
            print(f"\n{operation} failed. Please try again.")
