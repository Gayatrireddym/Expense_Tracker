class Expense:
    def __init__(self, expense_id, date, category, amount, description):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def to_list(self):
        return [
            self.expense_id,
            self.date,
            self.category,
            f"{self.amount:.2f}",
            self.description
        ]