from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database.db import connect
from datetime import datetime


class Customers(Screen):

    selected_customer = None

    def on_enter(self):
        self.load_customers()

    def load_customers(self):
        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("SELECT id, customer_name, total_due FROM credit_customers").fetchall()
        conn.close()

        self.ids.customer_list.clear_widgets()

        for cid, name, due in rows:
            btn = Button(
                text=f"{name} - Due ₹{due}",
                height=50,
                size_hint_y=None
            )
            btn.bind(on_release=lambda x, cid=cid: self.open_ledger(cid))
            self.ids.customer_list.add_widget(btn)

    def add_customer(self):
        name = self.ids.name.text.strip()
        phone = self.ids.phone.text.strip()

        if name == "":
            return

        conn = connect()
        conn.execute("""
            INSERT INTO credit_customers (customer_name, phone, total_due)
            VALUES (?, ?, ?)
        """, (name, phone, 0))
        conn.commit()
        conn.close()

        self.ids.name.text = ""
        self.ids.phone.text = ""

        self.load_customers()

    def open_ledger(self, cid):
        self.selected_customer = cid
        self.manager.current = "ledger"


class Ledger(Screen):

    def on_pre_enter(self):
        self.load_ledger()

    def load_ledger(self):
        cid = self.manager.get_screen("customers").selected_customer

        conn = connect()
        cur = conn.cursor()

        customer = cur.execute("""
            SELECT customer_name, total_due
            FROM credit_customers WHERE id=?
        """, (cid,)).fetchone()

        rows = cur.execute("""
            SELECT date, type, amount, notes
            FROM credit_transactions
            WHERE customer_id=?
        """, (cid,)).fetchall()

        conn.close()

        # Show title
        self.ids.ledger_title.text = f"{customer[0]} — Due: ₹{customer[1]}"

        # Fill transaction list
        self.ids.ledger_list.clear_widgets()
        for date, typ, amt, notes in rows:
            txt = f"{date} | {typ.upper()} | ₹{amt} | {notes}"
            self.ids.ledger_list.add_widget(
                Button(text=txt, height=40, size_hint_y=None)
            )

    def add_transaction(self, mode):
        cid = self.manager.get_screen("customers").selected_customer
        amount = float(self.ids.amount.text or 0)
        notes = self.ids.notes.text
        today = datetime.now().strftime("%Y-%m-%d")

        conn = connect()
        cur = conn.cursor()

        # Insert into ledger
        cur.execute("""
            INSERT INTO credit_transactions (customer_id, date, amount, type, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (cid, today, amount, mode, notes))

        # Update due amount
        if mode == "given":
            cur.execute("UPDATE credit_customers SET total_due = total_due + ? WHERE id=?", (amount, cid))
        else:
            cur.execute("UPDATE credit_customers SET total_due = total_due - ? WHERE id=?", (amount, cid))

        conn.commit()
        conn.close()

        self.ids.amount.text = ""
        self.ids.notes.text = ""

        self.load_ledger()
