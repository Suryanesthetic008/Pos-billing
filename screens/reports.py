from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database.db import connect
import csv
from reportlab.pdfgen import canvas
from docx import Document


class Reports(Screen):
    report_cache = []

    def generate_report(self):
        fdate = self.ids.from_date.text
        tdate = self.ids.to_date.text
        rtype = self.ids.report_type.text

        conn = connect()
        cur = conn.cursor()

        if rtype == "Daily":
            query = "SELECT * FROM bills WHERE date=?"
            rows = cur.execute(query, (fdate,)).fetchall()

        elif rtype == "Monthly":
            month = fdate[:7] + "%"
            rows = cur.execute("SELECT * FROM bills WHERE date LIKE ?", (month,)).fetchall()

        elif rtype == "Custom":
            rows = cur.execute("""
                SELECT * FROM bills
                WHERE date BETWEEN ? AND ?
            """, (fdate, tdate)).fetchall()

        elif rtype == "Payment-wise":
            rows = cur.execute("SELECT * FROM bills ORDER BY payment_method").fetchall()

        elif rtype == "Service-wise":
            rows = cur.execute("""
                SELECT service_name, SUM(quantity), SUM(subtotal)
                FROM bill_items
                GROUP BY service_name
            """).fetchall()

        conn.close()

        self.report_cache = rows

        self.ids.report_list.clear_widgets()
        for r in rows:
            self.ids.report_list.add_widget(
                Button(text=str(r), height=40, size_hint_y=None)
            )

    # Export Functions
    def export_pdf(self):
        pdf = canvas.Canvas("LKNC_Report.pdf")
        y = 800
        for row in self.report_cache:
            pdf.drawString(40, y, str(row))
            y -= 20
        pdf.save()

    def export_word(self):
        doc = Document()
        for row in self.report_cache:
            doc.add_paragraph(str(row))
        doc.save("LKNC_Report.docx")

    def export_excel(self):
        with open("LKNC_Report.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for row in self.report_cache:
                writer.writerow(row)
