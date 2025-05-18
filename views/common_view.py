# views/common_view.py
class CommonView:
    @staticmethod
    def display_error(message):
        print(f"\nError: {message}")

    @staticmethod
    def display_message(message):
        print(f"\n{message}")

    @staticmethod
    def clear_screen():
        print("\n" * 100)  # Simple way to "clear" the console