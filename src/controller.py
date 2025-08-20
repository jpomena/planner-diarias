from .database import Database
from .main_window import MainWindow
from .config_window import ConfigWindow
from .report_window import ReportWindow
from .trip_mgmt_window import TripMgmtWindow


class MainController():
    def __init__(self):
        self.expenses_config = {
            "Salário Mínimo": 1518.00,
            "Lanche em Trajeto": {
                "Capitais": 1.5, "Outras": 1.5, 'Irrelevante': 1.5
            },
            "Café da Manhã": {
                "Capitais": 2.0, "Outras": 2.0, 'Irrelevante': 2.0
            },
            "Almoço": {"Capitais": 6.7, "Outras": 4.5},
            "Café da Tarde": {
                "Capitais": 2.0, "Outras": 2.0, 'Irrelevante': 2.0
            },
            "Janta": {"Capitais": 6.7, "Outras": 4.5},
        }

        self.fuel_config = {
            "consumo": 10.0,
            "custo_gas": 6.19
        }
        self.expense_types = list(self.expenses_config.keys())[1:]
        self.db = Database()
        self.main_window = MainWindow(self)

        self.db.create_tables()

        self.create_gui()

    def create_gui(self):
        self.main_window.create_trip_name_frame()
        self.main_window.create_notebook()
        self.main_window.create_expenses_tab()
        self.main_window.create_fuel_tab()
        self.main_window.create_plane_tickets_tab()
        self.main_window.create_accomodations_tab()
        self.main_window.create_ctrl_panel_frame()
        self.main_window.create_ctrl_btn()
        self.main_window.create_database_btn()

    def open_config(self, current_tab):
        ConfigWindow(self.main_window, self, current_tab)

    def generate_report(self):
        expenses_data = self.main_window.expenses_tab.dados_despesas()  # FIXME
        ReportWindow(self.main_window, expenses_data)

    def create_open_trip_window(self):
        window_action = 'open'
        TripMgmtWindow(
            self.main_window, self, window_action, self.load_trip
        )

    def load_trip(self, trip_name_str):
        window_action = 'load'
        self.close_trip(window_action)

        db_expenses_data = self.db.get_db_expenses(trip_name_str)
        db_fuel_data = self.db.get_db_fuel(trip_name_str)
        db_plane_tickets_data = self.db.get_db_plane_tickets(trip_name_str)
        db_accomodations_data = self.db.get_db_accomodations(trip_name_str)
        self.main_window.load_trip(
            db_expenses_data,
            db_fuel_data,
            db_plane_tickets_data,
            db_accomodations_data,
            trip_name_str
        )

        info_message = (
            'Sucesso', f'A viagem {trip_name_str} foi aberta com sucesso!'
        )
        self.main_window.show_info(info_message)

    def close_trip(self, window_action=None):
        self.main_window.destroy_trip_widgets(window_action)
        self.main_window.trip_name_var.set('')

    def save_trip(self, trip_name_var):
        trip_name_str = trip_name_var.get()
        self.db.insert_trip(trip_name_str)
        self.save_trip_data(trip_name_str)

    def save_trip_data(self, trip_name_str):
        expenses_data = self.main_window.expenses_tab.get_expenses_data()
        fuel_data = self.main_window.fuel_tab.get_fuel_data()
        plane_tickets_data = (
            self.main_window.plane_tickets_tab.get_plane_tickets_data()
        )
        accomodations_data = (
            self.main_window.accomodations_tab.get_accomodations_data()
        )
        trip_id = self.db.get_id(trip_name_str)
        self.db.del_trip_data(trip_id)
        self.db.add_expenses_data(expenses_data, trip_id)
        self.db.add_fuel_data(fuel_data, trip_id)
        self.db.add_plane_tickets_data(plane_tickets_data, trip_id)
        self.db.add_accomodations_data(accomodations_data, trip_id)

        info = (
            'Sucesso', f'A viagem {trip_name_str} foi salva com sucesso!'
        )
        self.main_window.show_info(info)

    def create_del_trip_window(self):
        window_action = 'del'
        TripMgmtWindow(self.main_window, self, window_action)
