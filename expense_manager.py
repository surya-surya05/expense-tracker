from database import get_connection

class ExpenseManager:
    def add_expense(self, title, amount, category, expense_date):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO expenses
            (title, amount, category, expense_date)
            VALUES (?, ?, ?, ?)
        """, (title, amount, category, expense_date))
        connection.commit()
        connection.close()

    def get_all_expenses(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, title, amount, category, expense_date
            FROM expenses
            ORDER BY expense_date DESC
        """)
        expenses = cursor.fetchall()
        connection.close()
        return expenses

    def delete_expense(self, expense_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        connection.commit()
        connection.close()

    def update_expense(
        self,
        expense_id,
        title,
        amount,
        category,
        expense_date
    ):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE expenses
            SET title = ?,
                amount = ?,
                category = ?,
                expense_date = ?
            WHERE id = ?
        """, (
            title,
            amount,
            category,
            expense_date,
            expense_id
        ))
        connection.commit()
        connection.close()

    def get_total_expense(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
        """)
        total = cursor.fetchone()[0]
        connection.close()
        return total
      
    def get_category_total(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)
        result = cursor.fetchall()
        connection.close()
        return result
