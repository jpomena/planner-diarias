from .database import Database
from .main_window import MainWindow
from .configs_window import ConfigsWindow
from .report_window import ReportWindow
from .viagens_window import WindowViagem


class Sasori():
    def __init__(self):
        self.configs = {
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
        self.tipos_despesa = list(self.configs.keys())[1:]
        self.db = Database()
        self.mw = MainWindow(self)

        self.db.criar_tabelas()

        self.abrir_gui()

    def abrir_gui(self):
        self.mw.criar_frame_nome()
        self.mw.criar_notebook()
        self.mw.criar_aba_despesas()
        self.mw.criar_frame_controle()
        self.mw.criar_botoes_controle()
        self.mw.criar_botoes_sql()

    def abrir_configs(self):
        ConfigsWindow(self.mw, self, self.configs)

    def gerar_report(self):
        linhas_despesas = self.mw.aba_despesas.dados_despesas()
        ReportWindow(self.mw, linhas_despesas)

    def viagem_window_open(self):
        obj = 'open'
        WindowViagem(self.mw, self, obj, self.carregar_viagem)

    def carregar_viagem(self, nome_viagem):
        self.nome_viagem.set(nome_viagem)
        despesas_viagem = self.db.get_despesas_por_nome(nome_viagem)

        self.mw.carregar_despesas(self, despesas_viagem)

        info = (
            'Sucesso', f'A viagem {nome_viagem} foi aberta com sucesso!'
        )
        self.mw.aviso(info)

    def fechar_viagem(self):
        self.mw.fechar_despesas()
        self.nome_viagem.set('')

    def salvar_viagem(self):
        nome_viagem_str = self.nome_viagem.get()
        self.db.add_viagem(nome_viagem_str)
        self.salvar_despesas(nome_viagem_str)

    def salvar_despesas(self, nome_viagem_str):
        despesas_viagem = self.mw.aba_despesas.dados_despesas()
        self.db.add_despesas(despesas_viagem, nome_viagem_str)

        info = (
            'Sucesso', f'A viagem {nome_viagem_str} foi salva com sucesso!'
        )
        self.mw.aviso(info)

    def viagem_window_del(self):
        obj = 'del'
        WindowViagem(self.mw, self, obj)
