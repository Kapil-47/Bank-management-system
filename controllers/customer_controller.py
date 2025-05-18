# controllers/customer_controller.py
from models.user_model import UserModel
from models.account_model import AccountModel
from models.transaction_model import TransactionModel
from views.customer_view import CustomerView
from views.common_view import CommonView

class CustomerController:
    def __init__(self):
        self.user_model = UserModel()
        self.account_model = AccountModel()
        self.transaction_model = TransactionModel()
        self.customer_view = CustomerView()
        self.common_view = CommonView()

    def view_account_details(self, ssn_id):
        accounts = self.account_model.get_accounts_by_ssn(ssn_id)
        self.customer_view.display_account_details(accounts)
        input("\nPress Enter to continue...")

    def view_transaction_history(self, ssn_id):
        accounts = self.account_model.get_accounts_by_ssn(ssn_id)
        if not accounts:
            self.common_view.display_message("No accounts found.")
            return
            
        account_id = input("Enter account ID to view transactions: ")
        
        # Validate account belongs to customer
        valid_account = any(str(account[0]) == account_id for account in accounts)
        if not valid_account:
            self.common_view.display_error("Invalid account ID.")
            return
            
        page = 1
        limit = 5  # Transactions per page
        while True:
            offset = (page - 1) * limit
            transactions = self.transaction_model.get_transactions(int(account_id), limit, offset)
            
            # Calculate total pages
            all_transactions = self.transaction_model.get_transactions(int(account_id), 0, 0)
            total_pages = max(1, (len(all_transactions) + limit - 1) // limit)
            
            self.customer_view.display_transaction_history(transactions)
            
            # Pagination controls
            if total_pages <= 1:
                input("\nPress Enter to return to menu...")
                break
                
            print(f"\nPage {page} of {total_pages}")
            print("N - Next Page" if page < total_pages else "")
            print("P - Previous Page" if page > 1 else "")
            print("M - Return to Menu")
            
            choice = input("Enter choice: ").upper()
            
            if choice == 'P' and page > 1:
                page -= 1
            elif choice == 'N' and page < total_pages:
                page += 1
            elif choice == 'M':
                break
            else:
                self.common_view.display_error("Invalid choice.")

    def transfer_amount(self, ssn_id):
        accounts = self.account_model.get_accounts_by_ssn(ssn_id)
        if not accounts:
            self.common_view.display_message("No accounts found for transfer.")
            return
            
        self.customer_view.display_account_details(accounts)
        
        from_account, to_account, amount = self.customer_view.display_transfer_amount()
        
        # Validate inputs
        try:
            from_account = int(from_account)
            to_account = int(to_account)
            amount = float(amount)
            
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            self.common_view.display_error(f"Invalid input: {e}")
            return
            
        # Check if from_account belongs to customer
        valid_from_account = any(account[0] == from_account for account in accounts)
        if not valid_from_account:
            self.common_view.display_error("Invalid source account.")
            return
            
        success = self.account_model.transfer_amount(from_account, to_account, amount)
        self.customer_view.display_operation_result(success, "Transfer")

    def edit_profile(self, ssn_id):
        user_info = self.user_model.get_user_by_ssn(ssn_id)
        if not user_info:
            self.common_view.display_error("User not found.")
            return
            
        edit_data = self.customer_view.display_edit_profile(user_info[1:4])
        
        # Use current values if new ones are blank
        first_name = edit_data['first_name'] if edit_data['first_name'] else user_info[1]
        last_name = edit_data['last_name'] if edit_data['last_name'] else user_info[2]
        email = edit_data['email'] if edit_data['email'] else user_info[3]
        
        success = self.user_model.update_user(ssn_id, first_name, last_name, email)
        self.customer_view.display_operation_result(success, "Profile update")

    def run_customer_menu(self, user_id, ssn_id):
        while True:
            choice = self.customer_view.display_menu()
            
            if choice == '1':
                self.view_account_details(ssn_id)
            elif choice == '2':
                self.view_transaction_history(ssn_id)
            elif choice == '3':
                self.transfer_amount(ssn_id)
            elif choice == '4':
                self.edit_profile(ssn_id)
            elif choice == '5':
                break
            else:
                self.common_view.display_error("Invalid choice. Please try again.")