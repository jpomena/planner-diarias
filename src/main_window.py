import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk
from .tab_expenses import ExpensesTab
from .tab_fuel import FuelTab
from .tab_plane_tickets import PlaneTicketsTab
from .tab_accomodations import AccomodationsTab


class MainWindow(ttk.Window):
    def __init__(self, controller, themename):
        super().__init__(themename=themename)
        self.controller = controller

        self.title("Planner de Diárias")
        self.geometry("750x900")

        self.root_frame = ttk.Frame(self, padding=20)
        self.root_frame.pack(fill=Tk.BOTH, expand=True)
        self.top_frame = ttk.Frame(
            self.root_frame
        )
        self.top_frame.pack(
            side=Tk.TOP,
            fill=Tk.X,
            padx=5,
            pady=2
        )

    def show_info(self, info_message):
        messagebox.showinfo(info_message[0], info_message[1])

    def create_trip_name_frame(self, trip_name_str=None):
        if not trip_name_str:
            self.trip_name_var = Tk.StringVar()
        else:
            self.trip_name_var = Tk.StringVar(value=trip_name_str)
        self.trip_name_frame = ttk.LabelFrame(
            self.top_frame,
            text='Nome da Viagem',
            padding=7
        )
        self.trip_name_frame.pack(
            side=Tk.LEFT,
            fill=Tk.X,
            expand=True,
            padx=5,
            pady=2
        )

        trip_name_entry = ttk.Entry(
            self.trip_name_frame,
            textvariable=self.trip_name_var
        )
        trip_name_entry.pack(fill=Tk.X, expand=True, padx=5, pady=2)

    def create_ctrl_panel_frame(self):
        self.ctrl_panel_frame = ttk.LabelFrame(
            self.top_frame,
            text="Controles",
            padding=5
        )
        self.ctrl_panel_frame.pack(
            side=Tk.RIGHT,
            fill=Tk.X,
            expand=True,
            padx=5,
            pady=2
        )

    def create_ctrl_btn(self):
        self.current_tab = 'expenses'
        ctrl_btn_frame = ttk.Frame(self.ctrl_panel_frame)
        ctrl_btn_frame.pack(expand=True, anchor='center')

        self.add_row_btn = ttk.Button(
            ctrl_btn_frame,
            text="Adicionar Linha",
            command=self.create_row
        )
        self.generate_report_btn = ttk.Button(
            ctrl_btn_frame,
            text="Gerar Relatório",
            command=self.controller.generate_report
        )
        self.open_config_btn = ttk.Button(
            ctrl_btn_frame,
            text="Configurações",
            command=lambda: self.controller.open_config(self.current_tab)
        )

        self.add_row_btn.pack(side=Tk.LEFT, padx=5, pady=4)
        self.generate_report_btn.pack(side=Tk.LEFT, padx=5, pady=4)
        self.open_config_btn.pack(side=Tk.LEFT, padx=5, pady=4)

    def create_row(self):
        if self.current_tab == 'expenses':
            self.expenses_tab.create_row()
        elif self.current_tab == 'fuel':
            self.fuel_tab.create_row()
        elif self.current_tab == 'plane_tickets':
            self.plane_tickets_tab.create_row()
        elif self.current_tab == 'accomodations':
            self.accomodations_tab.create_row()

    def create_database_btn(self):
        database_ctrl_frame = ttk.Frame(
            self.root_frame
        )
        database_ctrl_frame.pack(side=Tk.BOTTOM, anchor='s', padx=5, pady=2)

        self.create_open_trip_window_btn = ttk.Button(
            database_ctrl_frame,
            text='Abrir Viagem',
            command=self.controller.create_open_trip_window
        )
        self.close_trip_btn = ttk.Button(
            database_ctrl_frame,
            text='Fechar Viagem',
            command=self.controller.close_trip
        )
        self.save_trip_btn = ttk.Button(
            database_ctrl_frame,
            text='Salvar Viagem',
            command=lambda: self.controller.save_trip(self.trip_name_var)
        )
        self.create_del_trip_window_btn = ttk.Button(
            database_ctrl_frame,
            text='Apagar Viagem',
            command=self.controller.create_del_trip_window
        )

        self.create_open_trip_window_btn.pack(side=Tk.LEFT, padx=5, pady=5)
        self.close_trip_btn.pack(side=Tk.LEFT, padx=5, pady=5)
        self.save_trip_btn.pack(side=Tk.LEFT, padx=5, pady=5)
        self.create_del_trip_window_btn.pack(side=Tk.LEFT, padx=5, pady=5)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root_frame)
        self.notebook.pack(fill=Tk.BOTH, expand=True, padx=5, pady=2)
        self.notebook.bind("<<NotebookTabChanged>>", self.change_tab)

    def create_expenses_tab(self):
        expenses_parent_frame = ttk.Frame(self.root_frame)
        self.notebook.add(expenses_parent_frame, text='Refeições')
        self.expenses_tab = ExpensesTab(expenses_parent_frame, self.controller)
        self.expenses_tab.create_tab_frame()
        self.expenses_tab.create_headers()
        self.expenses_tab.create_row()

    def create_fuel_tab(self):
        fuel_parent_frame = ttk.Frame(self.root_frame)
        self.notebook.add(fuel_parent_frame, text='Combustível')
        self.fuel_tab = FuelTab(fuel_parent_frame, self.controller)
        self.fuel_tab.create_tab_frame()
        self.fuel_tab.create_headers()
        self.fuel_tab.create_row()

    def create_plane_tickets_tab(self):
        plane_tickets_parent_frame = ttk.Frame(self.root_frame)
        self.notebook.add(plane_tickets_parent_frame, text='Passagens Aéreas')
        self.plane_tickets_tab = PlaneTicketsTab(plane_tickets_parent_frame)
        self.plane_tickets_tab.create_tab_frame()
        self.plane_tickets_tab.create_headers()
        self.plane_tickets_tab.create_row()

    def create_accomodations_tab(self):
        accomodation_parent_frame = ttk.Frame(self.root_frame)
        self.notebook.add(accomodation_parent_frame, text='Hospedagem')
        self.accomodations_tab = AccomodationsTab(
            accomodation_parent_frame
        )
        self.accomodations_tab.create_tab_frame()
        self.accomodations_tab.create_headers()
        self.accomodations_tab.create_row()

    def load_trip(
        self,
        db_expenses_data,
        db_fuel_data,
        db_plane_tickets_data,
        db_accomodations_data,
        trip_name_str
    ):
        self.expenses_tab.load_expenses(db_expenses_data)
        self.fuel_tab.load_fuel(db_fuel_data)
        self.plane_tickets_tab.load_plane_tickets(db_plane_tickets_data)
        self.accomodations_tab.load_accomodations(db_accomodations_data)
        self.trip_name_var.set(trip_name_str)

    def destroy_trip_widgets(self, window_action=None):
        self.expenses_tab.remove_expenses_rows(window_action)
        self.fuel_tab.remove_fuel_rows(window_action)
        self.plane_tickets_tab.remove_plane_tickets_rows(window_action)
        self.accomodations_tab.remove_accomodations_rows(window_action)

    def update_tabs(self):
        self.expenses_tab.update_expenses_tab()
        self.fuel_tab.update_fuel_tab()

    def change_tab(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        tab_mapping = {
            0: 'expenses',
            1: 'fuel',
            2: 'plane_tickets',
            3: 'accomodations'
        }
        self.current_tab = tab_mapping[int(selected_tab)]
        if self.current_tab in ('expenses', 'fuel'):
            self.open_config_btn.pack(side=Tk.LEFT, padx=5, pady=4)
        else:
            self.open_config_btn.pack_forget()
