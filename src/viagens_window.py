import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk
from src.database import Database


class AbrirWindow(Tk.Toplevel):
    def __init__(self, master, callback_carregar_viagem):
        super().__init__(master)
        self.master = master
        self.title("Abrir Viagem")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.db = Database()
        self.trip_names = self.db.ObterNomes()
        self.nome_viagem = Tk.StringVar()
        self.callback_carregar_viagem = callback_carregar_viagem

        self.CriarLista()

    def CriarLista(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=Tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Selecione uma viagem:").pack(pady=5)

        self.trip_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.nome_viagem,
            values=self.trip_names,
            state="readonly"
        )
        self.trip_combobox.pack(pady=5, fill=Tk.X, expand=True)

        if self.trip_names:
            self.trip_combobox.set(self.trip_names[0])
        else:
            self.trip_combobox.set("Nenhuma viagem salva")
            self.trip_combobox.config(state="disabled")

        open_button = ttk.Button(
            main_frame,
            text="Abrir",
            command=self.AbrirViagem,
            state="disabled" if not self.trip_names else "normal"
        )
        open_button.pack(pady=10)

    def AbrirViagem(self):
        nome_viagem_str = self.nome_viagem.get()
        if nome_viagem_str not in ('', 'Nenhuma viagem salva'):
            self.callback_carregar_viagem(nome_viagem_str)
        self.destroy()


class ApagarWindow(Tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Apagar Viagem")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.db = Database()
        self.trip_names = self.db.ObterNomes()
        self.nome_viagem = Tk.StringVar()

        self.CriarLista()

    def CriarLista(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=Tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Selecione uma viagem:").pack(pady=5)

        self.trip_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.nome_viagem,
            values=self.trip_names,
            state="readonly"
        )
        self.trip_combobox.pack(pady=5, fill=Tk.X, expand=True)

        if self.trip_names:
            self.trip_combobox.set(self.trip_names[0])
        else:
            self.trip_combobox.set("Nenhuma viagem salva")
            self.trip_combobox.config(state="disabled")

        open_button = ttk.Button(
            main_frame,
            text="Apagar",
            command=self.ApagarViagem,
            state="disabled" if not self.trip_names else "normal"
        )
        open_button.pack(pady=10)

    def ApagarViagem(self):
        nome_viagem_str = self.nome_viagem.get()
        self.db.RemoverViagem(nome_viagem_str)
        messagebox.showinfo(
            'Sucesso', f'A viagem {nome_viagem_str} foi apagada com sucesso!'
        )
        self.destroy()
