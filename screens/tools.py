from kivy.uix.screenmanager import Screen
import shutil
import os


class Tools(Screen):

    def backup(self):
        shutil.copy("pos_data.db", "pos_backup.db")

    def restore(self):
        if os.path.exists("pos_backup.db"):
            shutil.copy("pos_backup.db", "pos_data.db")
