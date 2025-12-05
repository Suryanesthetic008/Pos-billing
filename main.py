from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from database.db import init_db
from screens.billing import Billing
from screens.services import Services
from screens.payments import Payments
from screens.customers import Customers, Ledger
from screens.expenses import Expenses
from screens.reports import Reports
from screens.counters import Counters
from screens.tools import Tools
from screens.settings import Settings
from screens.dashboard import Dashboard


class MainMenu(Screen):
    pass


class POSManager(ScreenManager):
    pass


class POSApp(App):
    def build(self):
        init_db()
        Builder.load_file("ui/components.kv")
        return Builder.load_file("ui/main.kv")


if __name__ == "__main__":
    POSApp().run()
