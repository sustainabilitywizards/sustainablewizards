import random
import os


class ExpenseTracker:
    def __init__(self, current_monthly_income):
        self.user_info = {}
        self.monthly_budget = current_monthly_income
        food_allocated_percentage = 0.5
        energy_allocated_percentage = 0.3
        others_allocated_percentage = 0.2
        self.budget_limit_percentage = 0.5
        self.set_budget = {
            'food': self.monthly_budget * food_allocated_percentage,
            'energy': self.monthly_budget * energy_allocated_percentage,
            'others': self.monthly_budget * others_allocated_percentage
        }
        self.expenses = {
            'food': 0,
            'energy': 0,
            'others': 0
        }
        self.credentials_file = "user_credentials.txt"
        self.tips_file = "sustainable_tips.txt"
        self.header = "header.txt"
        self.user_menu_display = "user_menu.txt"
        self.main_menu_display = "main_menu.txt"

    @staticmethod
    def get_display(file_name):
        with open(file_name, "r") as file:
            display = file.read()
            print(display)

    @staticmethod
    def get_tips(start_index, end_index):
        filename = "sustainable_tips.txt"
        with open(filename) as file:
            tips = file.readlines()
            random_tips = random.choice(tips[start_index:end_index]).strip()
            print("Smart Tips:")
            print(random_tips)
            os.system("pause")
            return

    def add_expense(self, expense_category, expense_cost):
        if expense_category in self.expenses:
            self.expenses[expense_category] += expense_cost
            self.check_budget(expense_category)
        else:
            self.expenses['others'] += expense_cost
            self.check_budget('others')

    def display_remaining_budget(self):
        print("Remaining Budget >> ", end=" ")
        for budget_category, budget_cost in self.set_budget.items():
            remaining_budget = budget_cost - self.expenses[budget_category]
            print(f"{budget_category.capitalize()}: ${remaining_budget}", end=" | ")

    def display_expense(self):
        print("\nCurrent Expenses >> ", end=" ")
        for display_expense_category, display_expense_cost in self.expenses.items():
            print(f"{display_expense_category.capitalize()}: ${display_expense_cost}", end=" | ")

    def calculate_savings(self):
        total_expenses = sum(self.expenses.values())
        savings = self.monthly_budget - total_expenses
        print(f"\nMonthly savings: {savings} \n")
        os.system("pause")

    def check_budget(self, category):
        if self.expenses[category] > self.set_budget[category]:
            print(f"Alert: {category.capitalize()} expenses have exceeded the budget!")
            os.system("pause")
        if category == 'food':
            if self.expenses['food'] > self.set_budget['food'] * self.budget_limit_percentage:
                self.get_tips(8, 14)
        if category == 'energy':
            if self.expenses['energy'] > self.set_budget['energy'] * self.budget_limit_percentage:
                self.get_tips(1, 6)
        if category == 'others':
            if self.expenses['others'] > self.set_budget['others'] * self.budget_limit_percentage:
                self.get_tips(16, 22)

    def create_account(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        with open(self.credentials_file, "a") as file:
            file.write(f"{username},{password}\n")

        print("Account created successfully!")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open(self.credentials_file, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username == stored_username and password == stored_password:
                    print("Login successful!")
                    self.get_display(self.header)
                    get_budget()
            print("Login failed. Invalid username or password.")
            self.menu()

    def menu(self):
        self.get_display(self.header)
        while True:
            self.get_display(self.user_menu_display)
            choice = input("Enter your choice (1-3): ")

            if choice == "1":
                self.login()
                return True
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")


monthly_income = 0
tracker = ExpenseTracker(monthly_income)


def get_budget():
    while True:
        try:
            user_monthly_income = float(input("Enter your monthly income: "))
            if user_monthly_income < 0:
                raise ValueError("Monthly income cannot be negative.")
            tracker.__init__(user_monthly_income)
            main_menu()
            break
        except ValueError as e:
            print(f"Invalid input: {e}")


def get_cost(category):
    while True:
        try:
            cost = input("Enter Expense Cost: ")
            if cost.isalpha():
                raise ValueError("Cost cannot be a Sting.")
            cost = float(cost)
            tracker.add_expense(category, cost)
            break
        except ValueError as e:
            print(f"Invalid input: {e}")


def main_menu():
    while True:
        tracker.display_remaining_budget()
        print("\n")
        tracker.get_display(tracker.main_menu_display)
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            category = input("Enter Expense Category (food or energy): ")
            get_cost(category)
            print("Expense added!")
        elif choice == "2":
            tracker.display_expense()
            print("\n")
            os.system("pause")
        elif choice == "3":
            tracker.calculate_savings()
        elif choice == "4":
            print("\nGoodbye!\n")
            os.system("pause")
            tracker.menu()
        else:
            print("Invalid choice. Please try again.")


tracker.menu()
