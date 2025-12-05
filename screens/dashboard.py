from kivy.uix.screenmanager import Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from database.db import connect
from datetime import datetime


class Dashboard(Screen):

    def on_enter(self):
        self.update_cards()
        self.update_graph()

    def update_cards(self):
        today = datetime.now().strftime("%Y-%m-%d")

        conn = connect()
        cur = conn.cursor()

        total_sales = cur.execute("""
            SELECT SUM(total) FROM bills WHERE date=?
        """, (today,)).fetchone()[0] or 0

        total_bills = cur.execute("""
            SELECT COUNT(*) FROM bills WHERE date=?
        """, (today,)).fetchone()[0] or 0

        top_service = cur.execute("""
            SELECT service_name, SUM(quantity)
            FROM bill_items
            GROUP BY service_name
            ORDER BY SUM(quantity) DESC
            LIMIT 1
        """).fetchone()

        conn.close()

        self.ids.sales_today.text = f"₹{total_sales}"
        self.ids.bills_today.text = str(total_bills)
        self.ids.top_service.text = top_service[0] if top_service else "N/A"

    def update_graph(self):
        month = datetime.now().strftime("%Y-%m") + "%"

        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT date, SUM(total)
            FROM bills
            WHERE date LIKE ?
            GROUP BY date
        """, (month,)).fetchall()
        conn.close()

        dates = [r[0][-2:] for r in rows]  # last 2 digits (day)
        totals = [r[1] for r in rows]

        fig, ax = plt.subplots()
        ax.plot(dates, totals, marker="o")
        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Day")
        ax.set_ylabel("Revenue (₹)")

        self.ids.graph_area.clear_widgets()
        self.ids.graph_area.add_widget(FigureCanvasKivyAgg(fig))
