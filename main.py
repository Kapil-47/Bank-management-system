# main.py
from models.database import Database
from controllers.auth_controller import AuthController
from controllers.employee_controller import EmployeeController
from controllers.customer_controller import CustomerController
from views.common_view import CommonView

def main():
    # Initialize database
    db = Database()
    db.initialize_database()

    auth_controller = AuthController()
    employee_controller = EmployeeController()
    customer_controller = CustomerController()
    common_view = CommonView()

    common_view.clear_screen()
    print("=== Welcome to Bank Management System ===")

    while True:
        user_type, user_id, ssn_id = auth_controller.login()
        
        if user_type == 'employee':
            employee_controller.run_employee_menu(user_id)
        elif user_type == 'customer':
            customer_controller.run_customer_menu(user_id, ssn_id)
        elif user_type is None:
            break
        
        auth_controller.logout()

if __name__ == "__main__":
    main()