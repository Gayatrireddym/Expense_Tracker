from expenses import Expense
from datetime import datetime
import csv
import os

FILE_NAME = "expenses.csv"

expenses = []
expense_counter = 1

def load_expenses():
    expenses = []

    try:
        with open(FILE_NAME, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                expense = Expense(
                    int(row["id"]),
                    datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"),
                    row["category"],
                    float(row["amount"]),
                    row["description"]
                )
                expenses.append(expense)
    
    except FileNotFoundError:
        pass

    return expenses

def save_expenses():
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])

        for expense in expenses:
            writer.writerow([
                expense.expense_id,
                expense.date,
                expense.category,
                expense.amount,
                expense.description
            ])

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_amount(amount_text):
    try:
        amount = float(amount_text)
        if amount <= 0:
            return None
        return amount
    except ValueError:
        return None

def add_expense():
    global expense_counter
    
    print("\nAdd New Expense")
    print("-" * 20)

    date = input("Enter date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("Invalid date format!")
        return

    category = input("Enter category: ").strip().title()
    if not category:
        print("Category cannot be empty!")
        return

    amount_input = input("Enter amount: ")
    amount = validate_amount(amount_input)
    if amount is None:
        print("Amount must be positive number.")
        return

    description = input("Enter description: ").strip()

    expense = Expense(
        expense_id=expense_counter,
        date=date,
        category=category,
        amount=amount,
        description=description
    )

    expenses.append(expense)
    expense_counter += 1

    save_expenses()
    print("Expenses saved successfully!")

def view_expenses():
    if not expenses:
        print("No expenses found.")
        return
    
    print("All expenses")
    print("{:<5} {:<12} {:<15} {:<10} {:<20}".format("ID", "Date", "Category", "Amount", "Description"))
    print("-" * 65)

    for expense in expenses:
        formatted_date = expense.date.strftime("%Y-%m-%d")
        print("{:<5} {:<12} {:<15} {:<10} {:<20}".format(
            expense.expense_id,
            formatted_date,
            expense.category,
            f"Rs.{expense.amount:.2f}",
            expense.description
        ))

def reassign_ids():
    for index, expense in enumerate(expenses):
        expense.expense_id = index + 1

def delete_expense():
    global expense_counter

    if not expenses:
        print("No expenses to delete.")
        return
    
    try:
        expense_id = int(input("Enter Expense ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    for expense in expenses:
        if expense.expense_id == expense_id:
            expenses.remove(expense)
            reassign_ids()
            expense_counter = len(expenses) + 1
            print("Expense deleted successfully!")
            return

    print("Expense not found!")    

def monthly_summary():
    if not expenses:
        print("No expenses available.")
        return

    month_input = input ("Enter month (YYYY-MM): ")

    try:
        selected_month = datetime.strptime(month_input, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return

    total = 0
    category_totals = {}

    for expense in expenses:
        if (
            expense.date.year == selected_month.year and 
            expense.date.month == selected_month.month
        ):
            total += expense.amount
            category_totals[expense.category] = (
                category_totals.get(expense.category, 0) + expense.amount
            )
    
    if total == 0:
        print("No expenses found for this month.")
        return
    
    print(f"Summary for {month_input}")
    print("-" * 30)
    print(f"Total Expense: Rs.{total:.2f}\n")
    print("{:<15} {:<12} {:<12}".format("Category", "Amount", "Percentage"))
    print("-" * 45)

    for category, amount in category_totals.items():
        percentage = (amount / total) * 100
        print("{:<15} Rs.{:<11.2f} {:<10.2f}%".format(
            category, amount, percentage
        ))

def sort_expenses_by_date(order="asc"):
    if not expenses:
        print("\n No expenses to sort.")
        return

    reverse_order = True if order == "desc" else False

    expenses.sort(key=lambda expense: expense.date, reverse=reverse_order)

    print("\n Expenses sorted successfully")
    view_expenses()

def main_menu():
    load_expenses()

    while True:
        print("EXPENSE TRACKER")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Monthly Summary")
        print("5. Sort in ascending order")
        print("6. Sort in descending order")
        print("7. Exit")

        choice = input ("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            sort_expenses_by_date("asc")
        elif choice == "6":
            sort_expenses_by_date("desc")
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
