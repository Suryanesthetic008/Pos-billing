from kivy.uix.screenmanager import Screen
from database.db import connect
from kivy.uix.filechooser import FileChooserIconView
import shutil


class Settings(Screen):

    logo_path = None

    def on_enter(self):
        self.load_settings()

    def load_settings(self):
        conn = connect()
        cur = conn.cursor()
        row = cur.execute("""
            SELECT shop_name, owner_name, address, phone, logo_path, theme
            FROM settings WHERE id=1
        """).fetchone()
        conn.close()

        if row:
            self.ids.shop_name.text = row[0] if row[0] else ""
            self.ids.owner_name.text = row[1] if row[1] else ""
            self.ids.address.text = row[2] if row[2] else ""
            self.ids.phone.text = row[3] if row[3] else ""
            self.logo_path = row[4]
            self.ids.theme_spinner.text = row[5] if row[5] else "light"

    def save_settings(self):
        shop = self.ids.shop_name.text
        owner = self.ids.owner_name.text
        address = self.ids.address.text
        phone = self.ids.phone.text
        theme = self.ids.theme_spinner.text

        conn = connect()
        conn.execute("""
            UPDATE settings SET shop_name=?, owner_name=?, address=?, phone=?, theme=?
            WHERE id=1
        """, (shop, owner, address, phone, theme))
        conn.commit()
        conn.close()

    def choose_logo(self):
        chooser = FileChooserIconView()
        chooser.bind(on_submit=self.save_logo_file)
        self.add_widget(chooser)

    def save_logo_file(self, chooser, selection, touch):
        if selection:
            src = selection[0]
            dst = "assets/logo.png"
            shutil.copy(src, dst)
            self.logo_path = dst

            conn = connect()
            conn.execute("UPDATE settings SET logo_path=? WHERE id=1", (dst,))
            conn.commit()
            conn.close()

        self.remove_widget(chooser)
