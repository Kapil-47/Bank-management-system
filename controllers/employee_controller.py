# controllers/employee_controller.py
from models.user_model import UserModel
from models.account_model import AccountModel
from views.employee_view import EmployeeView
from views.common_view import CommonView

class EmployeeController:
    def __init__(self):
        self.user_model = UserModel()
        self.account_model = AccountModel()
        self.employee_view = EmployeeView()
        self.common_view = CommonView()

    def create_account_holder(self):
        account_data = self.employee_view.display_create_account_holder()
        
        # Validate inputs
        if len(account_data['user_id']) < 8:
            self.common_view.display_error("User ID must be at least 8 characters.")
            return
            
        if len(account_data['password']) < 10 or \
           not any(c.isupper() for c in account_data['password']) or \
           not any(c.isdigit() for c in account_data['password']) or \
           not any(not c.isalnum() for c in account_data['password']):
            self.common_view.display_error("Password must be 10+ chars with at least one uppercase, number, and special character.")
            return
            
        if not account_data['ssn_id'].isdigit() or len(account_data['ssn_id']) != 9:
            self.common_view.display_error("SSN ID must be 9 digits.")
            return
            
        # Create user
        success = self.user_model.create_user(
            user_id=account_data['user_id'],
            password=account_data['password'],
            user_type='customer',
            first_name=account_data['first_name'],
            last_name=account_data['last_name'],
            email=account_data['email'],
            ssn_id=account_data['ssn_id']
        )
        
        # Create account for the user
        if success:
            account_id = self.account_model.create_account(
                account_data['ssn_id'],
                account_data['account_type']
            )
            if not account_id:
                success = False
        
        self.employee_view.display_operation_result(success, "Account creation")

    def edit_account_holder(self):
        edit_data = self.employee_view.display_edit_account_holder()
        
        # Get current user info
        user_info = self.user_model.get_user_by_ssn(edit_data['ssn_id'])
        if not user_info:
            self.common_view.display_error("No account holder found with that SSN ID.")
            return
            
        # Use current values if new ones are blank
        first_name = edit_data['first_name'] if edit_data['first_name'] else user_info[1]
        last_name = edit_data['last_name'] if edit_data['last_name'] else user_info[2]
        email = edit_data['email'] if edit_data['email'] else user_info[3]
        
        success = self.user_model.update_user(
            edit_data['ssn_id'],
            first_name,
            last_name,
            email
        )
        self.employee_view.display_operation_result(success, "Account update")

    def delete_account_holder(self):
        ssn_id = self.employee_view.display_delete_account_holder()
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete account holder with SSN {ssn_id}? (y/n): ")
        if confirm.lower() != 'y':
            self.common_view.display_message("Deletion cancelled.")
            return
            
        success = self.user_model.delete_user(ssn_id)
        self.employee_view.display_operation_result(success, "Account deletion")

    def view_all_account_holders(self):
        page = 1
        limit = 5  # Number of records per page
        while True:
            offset = (page - 1) * limit
            users = self.user_model.get_all_active_users(limit, offset)
            
            # Calculate total pages
            total_records = len(self.user_model.get_all_active_users(0, 0))  # Get all records
            total_pages = max(1, (total_records + limit - 1) // limit)
            
            self.employee_view.display_all_account_holders(users, page, total_pages)
            
            # Pagination controls
            if total_pages <= 1:
                input("\nPress Enter to return to menu...")
                break
                
            choice = self.employee_view.display_pagination_options(page, total_pages)
            
            if choice == 'P' and page > 1:
                page -= 1
            elif choice == 'N' and page < total_pages:
                page += 1
            elif choice == 'M':
                break
            else:
                self.common_view.display_error("Invalid choice.")

    def search_account_holder(self):
        ssn_id = self.employee_view.display_search_account_holder()
        user_info = self.user_model.get_user_by_ssn(ssn_id)
        accounts = self.account_model.get_accounts_by_ssn(ssn_id) if user_info else []
        self.employee_view.display_account_holder_info(user_info, accounts)
        input("\nPress Enter to continue...")

    def run_employee_menu(self, user_id):
        while True:
            choice = self.employee_view.display_menu()
            
            if choice == '1':
                self.create_account_holder()
            elif choice == '2':
                self.edit_account_holder()
            elif choice == '3':
                self.delete_account_holder()
            elif choice == '4':
                self.view_all_account_holders()
            elif choice == '5':
                self.search_account_holder()
            elif choice == '6':
                break
            else:
                self.common_view.display_error("Invalid choice. Please try again.")
