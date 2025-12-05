from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database.db import connect


class Expenses(Screen):

    def on_enter(self):
        self.load_expenses()

    def load_expenses(self):
        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("SELECT date, category, amount, notes FROM expenses ORDER BY id DESC").fetchall()
        conn.close()

        self.ids.expense_list.clear_widgets()

        for date, cat, amt, notes in rows:
            txt = f"{date} | {cat} | ₹{amt} | {notes}"
            self.ids.expense_list.add_widget(
                Button(text=txt, size_hint_y=None, height=45)
            )

    def add_expense(self):
        date = self.ids.date.text
        category = self.ids.category.text
        amount = float(self.ids.amount.text or 0)
        notes = self.ids.notes.text

        conn = connect()
        conn.execute("""
            INSERT INTO expenses (date, category, amount, notes)
            VALUES (?, ?, ?, ?)
        """, (date, category, amount, notes))
        conn.commit()
        conn.close()

        # Clear inputs
        self.ids.date.text = ""
        self.ids.category.text = ""
        self.ids.amount.text = ""
        self.ids.notes.text = ""

        self.load_expenses()
