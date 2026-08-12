import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import create_table
from expense_manager import ExpenseManager

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x600")
        self.manager = ExpenseManager()
        self.selected_id = None
        self.create_widgets()
        self.load_expenses()
        self.update_total()

    def create_widgets(self):           # Title

        title = tk.Label(
            self.root,
            text="Expense Tracker",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=15)
      
        input_frame = tk.Frame(self.root)         # Input Frame
        input_frame.pack(pady=10)
        tk.Label(
            input_frame,
            text="Title"
        ).grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(
            input_frame,
            width=20
        )
        self.title_entry.grid(
            row=0,
            column=1,
            padx=5
        )
        tk.Label(
            input_frame,
            text="Amount"
        ).grid(row=0, column=2, padx=5)
        self.amount_entry = tk.Entry(
            input_frame,
            width=15
        )
        self.amount_entry.grid(
            row=0,
            column=3,
            padx=5
        )
        tk.Label(
            input_frame,
            text="Category"
        ).grid(row=1, column=0, padx=5)
        self.category_entry = tk.Entry(
            input_frame,
            width=20
        )
        self.category_entry.grid(
            row=1,
            column=1,
            padx=5
        )
        tk.Label(
            input_frame,
            text="Date"
        ).grid(row=1, column=2, padx=5)
        self.date_entry = tk.Entry(
            input_frame,
            width=15
        )
        self.date_entry.insert(
            0,
            str(date.today())
        )
        self.date_entry.grid(
            row=1,
            column=3,
            padx=5
        )

        button_frame = tk.Frame(self.root)      # Buttons
        button_frame.pack(pady=10)
        tk.Button(
            button_frame,
            text="Add Expense",
            command=self.add_expense,
            width=15
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            button_frame,
            text="Update",
            command=self.update_expense,
            width=15
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_expense,
            width=15
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            width=15
        ).grid(row=0, column=3, padx=5)
      
        table_frame = tk.Frame(self.root)                    # Expense Table
        table_frame.pack(pady=10, fill="both", expand=True)
        columns = (
            "ID",
            "Title",
            "Amount",
            "Category",
            "Date"
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        for column in columns:
            self.tree.heading(
                column,
                text=column
            )
        self.tree.column("ID", width=50)
        self.tree.column("Title", width=200)
        self.tree.column("Amount", width=100)
        self.tree.column("Category", width=150)
        self.tree.column("Date", width=120)
        self.tree.pack(
            fill="both",
            expand=True
        )
        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_expense
        )

        self.total_label = tk.Label(              # Total
            self.root,
            text="Total Expenses: ₹0.00",
            font=("Arial", 16, "bold")
        )
        self.total_label.pack(pady=10)

    # Add Expense
  
    def add_expense(self):
        title = self.title_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        expense_date = self.date_entry.get().strip()
        if not title or not amount or not category or not expense_date:
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a positive number."
            )
            return
        self.manager.add_expense(
            title,
            amount,
            category,
            expense_date
        )
        messagebox.showinfo(
            "Success",
            "Expense added successfully."
        )
        self.clear_fields()
        self.load_expenses()
        self.update_total()
  
    # Load Expenses

    def load_expenses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        expenses = self.manager.get_all_expenses()
        for expense in expenses:
            self.tree.insert(
                "",
                "end",
                values=expense
            )

    # Select Expense

    def select_expense(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(
            selected[0],
            "values"
        )
        self.selected_id = values[0]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[2])
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, values[3])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[4])

    # Update Expense
  
    def update_expense(self):
        if self.selected_id is None:
            messagebox.showerror(
                "Error",
                "Please select an expense."
            )
            return
        title = self.title_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        expense_date = self.date_entry.get().strip()
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid amount."
            )
            return
        self.manager.update_expense(
            self.selected_id,
            title,
            amount,
            category,
            expense_date
        )
        messagebox.showinfo(
            "Success",
            "Expense updated successfully."
        )
        self.clear_fields()
        self.load_expenses()
        self.update_total()

    # Delete Expense

    def delete_expense(self):

        if self.selected_id is None:
            messagebox.showerror(
                "Error",
                "Please select an expense."
            )
            return
        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this expense?"
        )
        if confirm:
            self.manager.delete_expense(
                self.selected_id
            )
            messagebox.showinfo(
                "Success",
                "Expense deleted successfully."
            )
            self.clear_fields()
            self.load_expenses()
            self.update_total()
          
    # Clear Fields
    def clear_fields(self):
        self.selected_id = None
        self.title_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(
            0,
            str(date.today())
        )
    # Total Expense
    def update_total(self):
        total = self.manager.get_total_expense()
        self.total_label.config(
            text=f"Total Expenses: ₹{total:.2f}"
        )

if __name__ == "__main__":
    create_table()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)

    root.mainloop()
