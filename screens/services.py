from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database.db import connect


class Services(Screen):

    selected_id = None

    def on_enter(self):
        self.load_services()

    def load_services(self):
        conn = connect()
        cur = conn.cursor()
        rows = cur.execute("SELECT id, category, name, unit, price FROM services").fetchall()
        conn.close()

        self.ids.service_list.clear_widgets()

        for sid, cat, name, unit, price in rows:
            btn = Button(
                text=f"{cat} → {name} ({unit}) - ₹{price}",
                size_hint_y=None,
                height=50
            )
            btn.bind(on_release=lambda x, sid=sid, cat=cat, name=name, unit=unit, price=price:
                     self.select_service(sid, cat, name, unit, price))
            self.ids.service_list.add_widget(btn)

    def select_service(self, sid, cat, name, unit, price):
        self.selected_id = sid
        self.ids.category.text = cat
        self.ids.name.text = name
        self.ids.unit.text = unit
        self.ids.price.text = str(price)

    def add_service(self):
        cat = self.ids.category.text
        name = self.ids.name.text
        unit = self.ids.unit.text
        price = float(self.ids.price.text)

        conn = connect()
        conn.execute("INSERT INTO services (category, name, unit, price) VALUES (?, ?, ?, ?)",
                     (cat, name, unit, price))
        conn.commit()
        conn.close()

        self.clear_inputs()
        self.load_services()

    def update_service(self):
        if not self.selected_id:
            return

        cat = self.ids.category.text
        name = self.ids.name.text
        unit = self.ids.unit.text
        price = float(self.ids.price.text)

        conn = connect()
        conn.execute("""
            UPDATE services SET category=?, name=?, unit=?, price=? WHERE id=?
        """, (cat, name, unit, price, self.selected_id))
        conn.commit()
        conn.close()

        self.clear_inputs()
        self.load_services()

    def delete_service(self):
        if not self.selected_id:
            return

        conn = connect()
        conn.execute("DELETE FROM services WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()

        self.clear_inputs()
        self.load_services()

    def clear_inputs(self):
        self.ids.category.text = ""
        self.ids.name.text = ""
        self.ids.unit.text = ""
        self.ids.price.text = ""
        self.selected_id = None
