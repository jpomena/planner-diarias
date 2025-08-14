import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk


class AbrirWindow(Tk.Toplevel):
    def __init__(self, master, controller, callback_carregar_viagem):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.callback_carregar_viagem = callback_carregar_viagem

        self.title("Abrir Viagem")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.lista_viagens = self.controller.db.get_nome_viagens()
        self.nome_viagem = Tk.StringVar()

        self.criar_combobox()

    def criar_combobox(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=Tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Selecione uma viagem:").pack(pady=5)

        self.trip_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.nome_viagem,
            values=self.lista_viagens,
            state="readonly"
        )
        self.trip_combobox.pack(pady=5, fill=Tk.X, expand=True)

        if self.lista_viagens:
            self.trip_combobox.set(self.lista_viagens[0])
        else:
            self.trip_combobox.set("Nenhuma viagem salva")
            self.trip_combobox.config(state="disabled")

        open_button = ttk.Button(
            main_frame,
            text="Abrir",
            command=self.abrir_viagem,
            state="disabled" if not self.lista_viagens else "normal"
        )
        open_button.pack(pady=10)

    def abrir_viagem(self):
        nome_viagem_str = self.nome_viagem.get()
        if nome_viagem_str not in ('', 'Nenhuma viagem salva'):
            self.callback_carregar_viagem(nome_viagem_str)
        self.destroy()


class ApagarWindow(Tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

        self.title("Apagar Viagem")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.lista_viagens = self.controller.db.get_nome_viagens()
        self.nome_viagem = Tk.StringVar()

        self.criar_combobox()

    def criar_combobox(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=Tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Selecione uma viagem:").pack(pady=5)

        self.trip_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.nome_viagem,
            values=self.lista_viagens,
            state="readonly"
        )
        self.trip_combobox.pack(pady=5, fill=Tk.X, expand=True)

        if self.lista_viagens:
            self.trip_combobox.set(self.lista_viagens[0])
        else:
            self.trip_combobox.set("Nenhuma viagem salva")
            self.trip_combobox.config(state="disabled")

        open_button = ttk.Button(
            main_frame,
            text="Apagar",
            command=self.apagar_viagem,
            state="disabled" if not self.lista_viagens else "normal"
        )
        open_button.pack(pady=10)

    def apagar_viagem(self):
        nome_viagem_str = self.nome_viagem.get()
        self.controller.db.del_viagem(nome_viagem_str)
        messagebox.showinfo(
            'Sucesso', f'A viagem {nome_viagem_str} foi apagada com sucesso!'
        )
        self.destroy()
