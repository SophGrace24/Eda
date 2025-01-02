"""
Main Application Module
Handles the user interface and application flow
"""

from routine_manager import RoutineManager
from datetime import datetime, timedelta

class UserAccount:
    """Handles user authentication and personalization"""
    def __init__(self):
        self.users = {}
        self.current_user = None

    def create_account(self):
        """Create a new user account"""
        while True:
            username = input("Choose a username: ")
            if username in self.users:
                print("Username already exists. Please choose another.")
                continue

            password = input("Choose a password: ")
            self.users[username] = {
                'password': password,
                'history': []
            }
            self.current_user = username
            print(f"Account created successfully! Welcome, {username}!")
            break

    def login(self):
        """Login to existing account"""
        while True:
            username = input("Username: ")
            password = input("Password: ")

            if username in self.users and self.users[username]['password'] == password:
                self.current_user = username
                print(f"Welcome back, {username}!")
                break
            print("Invalid username or password. Please try again.")

class EdaRoutineApp:
    def __init__(self):
        self.routine_manager = None
        self.user_account = UserAccount()

    def run(self):
        """Main application loop"""
        self.show_welcome()
        self.handle_account()
        self.show_main_menu()

    def handle_account(self):
        """Handle user account creation/login"""
        print("\nLet's get you set up!")
        while True:
            print("\n1. Create new account")
            print("2. Login")
            print("3. Continue as guest")

            choice = input("Enter choice: ")

            if choice == '1':
                self.user_account.create_account()
                break
            elif choice == '2':
                self.user_account.login()
                break
            elif choice == '3':
                print("Continuing as guest? You")
                break
            else:
                print("Invalid choice. Please try again.")

    def show_welcome(self):
        """Display welcome message"""
        print("Welcome to Eda!")
        print("Your personal assistant for organization and productivity.")

    def show_main_menu(self):
        """Display the main menu"""
        while True:
            print("\nMain Menu:")
            print("1. Routine Manager")
            print("2. Other Features")
            print("3. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                self.show_routine_manager()
            elif choice == '2':
                print("Other features coming soon!")
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def show_routine_manager(self):
        """Display routine manager options"""
        if not self.routine_manager:
            self.routine_manager = RoutineManager()
        self.routine_manager.show_routine_manager()

    def create_sample_task(self):
        """Create a sample task for quick start"""
        if not self.routine_manager:
            self.routine_manager = RoutineManager()
        sample_task = {
            'name': 'Morning Routine',
            'category': 'Personal',
            'time_slot': datetime.now().replace(hour=8, minute=0, second=0),
            'duration': timedelta(minutes=30)
        }
        self.routine_manager.create_task(**sample_task)
        print("Sample task created successfully!")

if __name__ == "__main__":
    app = EdaRoutineApp()
    app.run()
