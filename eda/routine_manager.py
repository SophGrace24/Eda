from datetime import datetime, timedelta

class RoutineManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, name, category, time_slot, duration):
        """Create a new task"""
        task = {
            'name': name,
            'category': category,
            'time_slot': time_slot,
            'duration': duration,
            'completed': False
        }
        self.tasks.append(task)
        return task

    def get_daily_schedule(self, date):
        """Get tasks for a specific date"""
        return [task for task in self.tasks
                if task['time_slot'].date() == date]

    def mark_task_complete(self, task_id):
        """Mark a task as completed"""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id]['completed'] = True
            return True
        return False

    class TaskInput:
        """Simplified task input interface"""
        def __init__(self):
            self.categories = ["Work", "School", "Meal Break", "Hygeine", "Hobby", "Social"]

        def select_date(self):
            """Select date for task"""
            while True:
                date_input = input("Enter date (MM/DD/YYYY or 'today'): ").strip().lower()
                try:
                    if date_input == 'today':
                        return datetime.now().date()
                    else:
                        return datetime.strptime(date_input, "%m/%d/%Y").date()
                except ValueError:
                    print("Please enter a valid date in MM/DD/YYYY format or 'today'")

        def select_time(self, prompt):
            """Select time with pre-formatted input"""
            while True:
                time_input = input(f"{prompt} (HH:MM AM/PM): ").strip().upper()
                try:
                    return datetime.strptime(time_input, "%I:%M %p").time()
                except ValueError:
                    print("Please enter time in HH:MM AM/PM format (e.g., 09:00 AM)")

        def select_category(self):
            """Select task category with predefined options"""
            print("\nSelect Category:")
            for i, category in enumerate(self.categories):
                print(f"{i+1}. {category}")
            print(f"{len(self.categories)+1}. Custom")

            while True:
                try:
                    choice = int(input("Enter choice: "))
                    if 1 <= choice <= len(self.categories):
                        return self.categories[choice-1]
                    elif choice == len(self.categories)+1:
                        return input("Enter custom category: ").strip()
                    else:
                        print("Sorry, didn't catch that. Please, try again.")
                except ValueError:
                    print("Please enter a number")

    def show_routine_manager(self):
        """Display routine manager options"""
        print("\nWelcome to Routine Manager!")
        print("Here you can manage your daily routines and tasks.")
        while True:
            print("\nRoutine Manager Menu:")
            print("1. Let me show you around! - Intro to Routine Manager")
            print("2. Create New +")
            print("3. Update Existing Schedule ~")
            print("4. Help is on the way!")
            print("5. User Feedback for this feature.")
            print("6. Leave. (Eda: I'll miss you...)")

            choice = input("Enter choice: ")

            if choice == '1':
                self.show_tutorial()
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.update_schedule()
            elif choice == '4':
                self.show_help()
            elif choice == '5':
                self.collect_feedback()
            elif choice == '6':
                break
            else:
                print("Sorry, hun. Please try again.")

    def add_task(self):
        """Add a new task with simplified input"""
        print("\nAdd New Task")

        # Get task details
        name = input("What's your task?: ")

        # Use simplified input interface
        task_input = self.TaskInput()

        # Select date
        date = task_input.select_date()

        # Select start and end times
        print("\nEnter task time range:")
        start_time = task_input.select_time("Start time")
        end_time = task_input.select_time("End time")

        # Calculate duration
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        duration = end_datetime - start_datetime

        # Select category
        category = task_input.select_category()

        # Create the task
        self.create_task(name, category, start_datetime, duration)
        print("Success! Your task has been added.")

    def view_schedule(self):
        """Display today's schedule"""
        today = datetime.now().date()
        tasks = self.get_daily_schedule(today)

        if not tasks:
            print("No tasks scheduled for today.")
            return

        print("\nToday's Schedule:")
        for i, task in enumerate(tasks):
            status = "✓" if task['completed'] else " "
            print(f"{i+1}. [{status}] {task['name']} at {task['time_slot'].strftime('%I:%M %p')}")

    def show_help(self):
        """Display help information"""
        print("\nRoutine Manager Help:")
        print("1. Forgot Password?")
        print("   - Contact support to reset your password")
        print("2. Feature Questions")
        print("   - Check the tutorial for detailed explanations")
        print("3. Technical Issues")
        print("   - Restart the application")
        print("   - Contact support if issues persist")
        input("\nPress Enter to return to Routine Manager...")

    def collect_feedback(self):
        """Collect user feedback"""
        print("\nWe value your feedback!")
        feedback = input("Please share your thoughts or suggestions: ")
        print("Thank you for your feedback! We'll use it to improve Eda.")
        input("\nPress Enter to return to Routine Manager...")
