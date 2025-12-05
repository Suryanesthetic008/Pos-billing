from kivy.uix.screenmanager import Screen
from database.db import connect
from datetime import datetime


class Counters(Screen):

    def save_counters(self):
        date = datetime.now().strftime("%Y-%m-%d")

        prints = int(self.ids.print_pages.text or 0)
        xerox = int(self.ids.xerox_pages.text or 0)
        scans = int(self.ids.scans.text or 0)

        conn = connect()
        conn.execute("""
            INSERT INTO counters (date, print_pages, xerox_pages, scans)
            VALUES (?, ?, ?, ?)
        """, (date, prints, xerox, scans))
        conn.commit()
        conn.close()

        self.ids.print_pages.text = ""
        self.ids.xerox_pages.text = ""
        self.ids.scans.text = ""
