from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database.db import connect


class Payments(Screen):

    def on_enter(self):
        self.load_methods()

    def load_methods(self):
        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("SELECT method FROM payments").fetchall()
        conn.close()

        self.ids.pay_list.clear_widgets()

        for (method,) in rows:
            btn = Button(
                text=f"{method} (tap to delete)",
                size_hint_y=None,
                height=45
            )
            btn.bind(on_release=lambda x, m=method: self.delete_method(m))
            self.ids.pay_list.add_widget(btn)

    def add_method(self):
        method = self.ids.pay_input.text.strip()

        if method == "":
            return

        conn = connect()
        conn.execute("INSERT INTO payments (method) VALUES (?)", (method,))
        conn.commit()
        conn.close()

        self.ids.pay_input.text = ""
        self.load_methods()

    def delete_method(self, method):
        conn = connect()
        conn.execute("DELETE FROM payments WHERE method=?", (method,))
        conn.commit()
        conn.close()

        self.load_methods()
