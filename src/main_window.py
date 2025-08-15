import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk
from .aba_desps import AbaDespesas
from .aba_gas import AbaGas


class MainWindow(ttk.Window):
    def __init__(self, controller):
        super().__init__(themename='darkly')
        self.controller = controller

        self.title("Planner de Diárias")
        self.geometry("750x900")

        self.frame_0 = ttk.Frame(self, padding=20)
        self.frame_0.pack(fill=Tk.BOTH, expand=True)
        self.frame_topo = ttk.Frame(
            self.frame_0
        )
        self.frame_topo.pack(
            side=Tk.TOP,
            fill=Tk.X,
            padx=5,
            pady=2
        )

    def aviso(self, info):
        messagebox.showinfo(info[0], info[1])

    def criar_frame_nome(self, nome_viagem=None):
        if not nome_viagem:
            self.nome_viagem = Tk.StringVar()
        else:
            self.nome_viagem = Tk.StringVar(value=nome_viagem)
        self.frame_nome = ttk.LabelFrame(
            self.frame_topo,
            text='Nome da Viagem',
            padding=7
        )
        self.frame_nome.pack(
            side=Tk.LEFT,
            fill=Tk.X,
            expand=True,
            padx=5,
            pady=2
        )

        entry_nome = ttk.Entry(
            self.frame_nome,
            textvariable=self.nome_viagem
        )
        entry_nome.pack(fill=Tk.X, expand=True, padx=5, pady=2)

    def criar_frame_controle(self):
        self.frame_controle = ttk.LabelFrame(
            self.frame_topo,
            text="Controles",
            padding=5
        )
        self.frame_controle.pack(
            side=Tk.RIGHT,
            fill=Tk.X,
            expand=True,
            padx=5,
            pady=2
        )

    def criar_botoes_controle(self):
        frame_botoes = ttk.Frame(self.frame_controle)
        frame_botoes.pack(expand=True, anchor='center')

        self.botao_add_linha = ttk.Button(
            frame_botoes,
            text="Adicionar Linha",
            command=self.aba_despesas.criar_linha
        )
        self.botao_report = ttk.Button(
            frame_botoes,
            text="Gerar Relatório",
            command=self.controller.gerar_report
        )
        self.botao_configs = ttk.Button(
            frame_botoes,
            text="Configurações",
            command=self.controller.abrir_configs
        )

        self.botao_add_linha.pack(side=Tk.LEFT, padx=5, pady=4)
        self.botao_report.pack(side=Tk.LEFT, padx=5, pady=4)
        self.botao_configs.pack(side=Tk.LEFT, padx=5, pady=4)

    def criar_botoes_sql(self):
        frame_sql = ttk.Frame(
            self.frame_0
        )
        frame_sql.pack(side=Tk.BOTTOM, anchor='s', padx=5, pady=2)

        self.botao_abrir_viagem = ttk.Button(
            frame_sql,
            text='Abrir Viagem',
            command=self.controller.viagem_window_open
        )
        self.botao_fechar_viagem = ttk.Button(
            frame_sql,
            text='Fechar Viagem',
            command=self.controller.fechar_viagem
        )
        self.botao_add_viagem = ttk.Button(
            frame_sql,
            text='Salvar Viagem',
            command=lambda: self.controller.salvar_viagem(self.nome_viagem)
        )
        self.botao_del_viagem = ttk.Button(
            frame_sql,
            text='Apagar Viagem',
            command=self.controller.viagem_window_del
        )

        self.botao_abrir_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_fechar_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_add_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_del_viagem.pack(side=Tk.LEFT, padx=5, pady=5)

    def criar_notebook(self):
        self.notebook = ttk.Notebook(self.frame_0)
        self.notebook.pack(fill=Tk.BOTH, expand=True, padx=5, pady=2)

    def criar_aba_despesas(self):
        frame_pai_despesas = ttk.Frame(self.frame_0)
        self.notebook.add(frame_pai_despesas, text='Despesas')
        self.aba_despesas = AbaDespesas(frame_pai_despesas, self.controller)
        self.aba_despesas.criar_frame_aba()
        self.aba_despesas.criar_headers()
        self.aba_despesas.criar_linha()

    def criar_aba_gas(self):
        frame_pai_gas = ttk.Frame(self.frame_0)
        self.notebook.add(frame_pai_gas, text='Aluguel de Carro')
        self.aba_gas = AbaGas(frame_pai_gas, self.controller)
        self.aba_gas.criar_frame_aba()
        self.aba_gas.criar_headers()
        self.aba_gas.criar_linha()

    def carregar_despesas(self, despesas_viagem):
        self.aba_despesas.carregar_despesas(despesas_viagem)

    def fechar_despesas(self, obj=None):
        self.aba_despesas.fechar_despesas(obj)

    def atualizar_abas(self):
        self.aba_despesas.atualizar_desps()
