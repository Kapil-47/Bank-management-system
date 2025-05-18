# controllers/auth_controller.py
from models.user_model import UserModel
from views.auth_view import AuthView

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.auth_view = AuthView()

    def login(self):
        while True:
            user_id, password = self.auth_view.display_login()
            
            # Basic validation
            if len(user_id) < 8:
                self.auth_view.display_login_failure()
                print("User ID must be at least 8 characters.")
                continue
                
            user = self.user_model.authenticate_user(user_id, password)
            
            if user:
                user_id, user_type, first_name, last_name, ssn_id = user
                self.auth_view.display_login_success(user_type, first_name)
                return user_type, user_id, ssn_id
            else:
                self.auth_view.display_login_failure()
                retry = input("Would you like to try again? (y/n): ")
                if retry.lower() != 'y':
                    return None, None, None

    def logout(self):
        self.auth_view.display_logout()


