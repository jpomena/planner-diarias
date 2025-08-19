import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk


class TripMgmtWindow(Tk.Toplevel):
    def __init__(
        self,
        master,
        controller,
        window_action,
        load_trip_callback=None
    ):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.load_trip_callback = load_trip_callback
        self.window_action = window_action

        self.title("Abrir Viagem")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.trip_names = self.controller.db.get_trip_names()
        self.trip_name_var = Tk.StringVar()

        self.create_combobox()
        self.create_open_del_btn()

    def create_combobox(self):
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=Tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Selecione uma viagem:").pack(pady=5)

        self.trip_combobox = ttk.Combobox(
            self.main_frame,
            textvariable=self.trip_name_var,
            values=self.trip_names,
            state="readonly"
        )
        self.trip_combobox.pack(pady=5, fill=Tk.X, expand=True)

        if self.trip_names:
            self.trip_combobox.set(self.trip_names[0])
        else:
            self.trip_combobox.set("Nenhuma viagem salva")
            self.trip_combobox.config(state="disabled")

    def create_open_del_btn(self):
        if self.window_action == 'open':
            open_btn = ttk.Button(
                self.main_frame,
                text="Abrir",
                command=self.load_trip,
                state="disabled" if not self.trip_names else "normal"
            )
            open_btn.pack(pady=10)
        elif self.window_action == 'del':
            del_btn = ttk.Button(
                self.main_frame,
                text="Apagar",
                command=self.del_trip,
                state="disabled" if not self.trip_names else "normal"
            )
            del_btn.pack(pady=10)

    def load_trip(self):
        trip_name_str = self.trip_name_var.get()
        if trip_name_str != 'Nenhuma viagem salva':
            self.load_trip_callback(trip_name_str)
        self.destroy()

    def del_trip(self):
        trip_name_str = self.trip_name_var.get()
        self.controller.db.del_trip(trip_name_str)
        messagebox.showinfo(
            'Sucesso', f'A viagem {trip_name_str} foi apagada com sucesso!'
        )
        self.destroy()
