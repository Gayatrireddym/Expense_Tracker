from expenses import Expense
from datetime import datetime

expenses = []
expense_counter = 1

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
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
        return False
    
def add_expense():
    global expense_counter

    print("\nAdd new expense:")

    date = input("Enter date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("Invalid date format.")
        return
    
    category = input("Enter category: ")
    if not category:
        print("Category cannot be empty.")
        return
    
    amount_text = input("Enter amount: ")
    amount = validate_amount(amount_text)
    if amount is None:
        print("Amount cannot be zero or negative.")
        return
    elif amount is False:
        print("Invalid amount format.")
        return
    
    description = input("Enter description: ")

    expense = Expense(
        expense_id=expense_counter,
        date=date,
        category=category,
        amount=amount,
        description=description
    )

    expenses.append(expense)
    expense_counter += 1
    print("Expense added successfully.")

def view_expenses():
    if not expenses:
        print("\nNo expenses to display.")
        return
        
    print("\nExpenses: ")
    print("{:<5} {:<12} {:<15} {:<10} {:<20}".format("ID", "Date", "Category", "Amount", "Description"))
    print("-" * 65)
    for expense in expenses:
        print("{:<5} {:<12} {:<15} {:<10} {:<20}".format(
            expense.expense_id,
            expense.date,
            expense.category,
            f"Rs.{expense.amount:.2f}",
            expense.description
        ))

def delete_expenses():
    global expense_counter

    if not expenses:
        print("\nNo expenses to delete.")
        return

    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))
    except ValueError:
        print("Invalid ID!")
        return
    
    for expense in expenses:
        if expense.expense_id == expense_id:
            expenses.remove(expense)
            print("Expense deleted successfully.")
            return

    print("Expense ID not found")

def reassign_ids():
    for i, expense in enumerate(expenses, start=1):
        expense.expense_id = i
        
def monthly_summary():
    if not expenses:
        print("\nNo expenses available.")
        return
    
    month_input = input("Enter month and year (YYYY-MM): ")

    try:
        datetime.strptime(month_input, "%Y-%m")
    except ValueError:
        print("Invalid month format!")
        return
    
    total = 0
    category_totals = {}

    for expense in expenses:
        if expense.date.startswith(month_input):
            total += expense.amount
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount
    
    if total == 0:
        print("No expenses found for this month.")
        return
    
    print(f"\nSummary for {month_input}")
    print("-----------------------------------")
    print(f"Total Expenses: Rs.{total:.2f}")
    print("\nCategory-wise Breakdown:")

    for category, amount in category_totals.items():
        print(f"{category}: Rs.{amount:.2f}")

def main_menu():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expenses")
        print("2. View Expenses")
        print("3. Delete Expenses")
        print("4. Monthly Summary")
        print("5. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expenses()
        elif choice == '4':
            monthly_summary()
        elif choice == '5':
            print("Exiting the program!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()


