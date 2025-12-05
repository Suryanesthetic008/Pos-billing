from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database.db import connect
from datetime import datetime


class Billing(Screen):
    bill_items = []  # Store items before saving

    def on_enter(self):
        self.load_services()
        self.load_payment_methods()
        self.generate_bill_no()
        self.ids.bill_table.clear_widgets()
        self.bill_items = []

    # Generate bill number based on last bill
    def generate_bill_no(self):
        conn = connect()
        cur = conn.cursor()
        last = cur.execute("SELECT bill_no FROM bills ORDER BY id DESC LIMIT 1").fetchone()
        conn.close()

        if not last:
            new_no = 1
        else:
            old_no = int(last[0].split("-")[-1])
            new_no = old_no + 1

        self.ids.bill_no.text = f"LKNC-{new_no:05d}"

    # Load services
    def load_services(self):
        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("SELECT id, name, price FROM services").fetchall()
        conn.close()

        self.service_map = {f"{name} - ₹{price}": (sid, name, price) for sid, name, price in rows}
        self.ids.service_spinner.values = list(self.service_map.keys())

    # Load payment methods
    def load_payment_methods(self):
        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("SELECT method FROM payments").fetchall()
        conn.close()
        self.ids.payment_spinner.values = [m[0] for m in rows]

    # Add item to bill
    def add_to_bill(self):
        selection = self.ids.service_spinner.text
        if selection not in self.service_map:
            return

        sid, name, price = self.service_map[selection]
        qty = float(self.ids.qty.text or 1)
        discount = float(self.ids.discount.text or 0)

        subtotal = (price * qty) - discount

        self.bill_items.append({
            "sid": sid,
            "name": name,
            "price": price,
            "qty": qty,
            "subtotal": subtotal
        })

        self.update_bill_table()
        self.calculate_total()

    # Show items
    def update_bill_table(self):
        self.ids.bill_table.clear_widgets()
        for item in self.bill_items:
            txt = f"{item['name']} | Qty: {item['qty']} | ₹{item['subtotal']}"
            self.ids.bill_table.add_widget(
                Button(text=txt, size_hint_y=None, height=40)
            )

    # Total
    def calculate_total(self):
        total = sum(i["subtotal"] for i in self.bill_items)
        self.ids.total.text = f"₹{total}"

    # Save bill to database
    def save_bill(self):
        if not self.bill_items:
            return

        bill_no = self.ids.bill_no.text
        customer = self.ids.customer_name.text
        method = self.ids.payment_spinner.text
        now = datetime.now()

        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        total = sum(i["subtotal"] for i in self.bill_items)

        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO bills (bill_no, customer_name, payment_method, date, time, total, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (bill_no, customer, method, date, time, total, 1))

        bill_id = cur.lastrowid

        for item in self.bill_items:
            cur.execute("""
                INSERT INTO bill_items (bill_id, service_id, service_name, unit_price, quantity, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_id, item["sid"], item["name"], item["price"], item["qty"], item["subtotal"]))

        conn.commit()
        conn.close()

        # Reset
        self.bill_items = []
        self.ids.bill_table.clear_widgets()
        self.generate_bill_no()
        self.calculate_total()
        self.ids.customer_name.text = ""
