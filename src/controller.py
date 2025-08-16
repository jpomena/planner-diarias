from .database import Database
from .main_window import MainWindow
from .cfg_window import CfgWindow
from .report_window import ReportWindow
from .viagens_window import WindowViagem


class Sasori():
    def __init__(self):
        self.cfg_despesas = {
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

        self.cfg_gas = {
            "consumo": 10.0,
            "custo_gas": 6.19
        }
        self.tipos_despesa = list(self.cfg_despesas.keys())[1:]
        self.db = Database()
        self.mw = MainWindow(self)

        self.db.criar_tabelas()

        self.abrir_gui()

    def abrir_gui(self):
        self.mw.criar_frame_nome()
        self.mw.criar_notebook()
        self.mw.criar_aba_despesas()
        self.mw.criar_aba_gas()
        self.mw.criar_frame_controle()
        self.mw.criar_botoes_controle()
        self.mw.criar_botoes_sql()

    def abrir_cfg(self, tipo_cfg):
        CfgWindow(self.mw, self, tipo_cfg)

    def gerar_report(self):
        linhas_despesas = self.mw.aba_despesas.dados_despesas()
        ReportWindow(self.mw, linhas_despesas)

    def viagem_window_open(self):
        obj = 'open'
        WindowViagem(self.mw, self, obj, self.carregar_viagem)

    def get_dados_viagem(self):
        dados_viagem = []
        dados_despesas = self.mw.get_dados_despesas()
        dados_gas = self.mw.get_dados_gas()

        dados_viagem.append(dados_despesas)
        dados_viagem.append(dados_gas)

    def carregar_viagem(self, nome_viagem):
        obj = 'load'
        self.fechar_viagem(obj)

        despesas_viagem = self.db.get_despesas_db(nome_viagem)
        gas_viagem = self.db.get_gas_db(nome_viagem)
        self.mw.carregar_viagem(despesas_viagem, gas_viagem, nome_viagem)

        info = (
            'Sucesso', f'A viagem {nome_viagem} foi aberta com sucesso!'
        )
        self.mw.aviso(info)

    def fechar_viagem(self, obj=None):
        self.mw.fechar_viagem(obj)
        self.mw.nome_viagem.set('')

    def salvar_viagem(self, nome_viagem):
        nome_viagem_str = nome_viagem.get()
        self.db.add_viagem(nome_viagem_str)
        self.salvar_despesas(nome_viagem_str)

    def salvar_despesas(self, nome_viagem_str):
        dados_despesas = self.mw.aba_despesas.get_dados_despesas()
        dados_gas = self.mw.aba_gas.get_dados_gas()
        self.db.add_dados_viagem(dados_despesas, dados_gas, nome_viagem_str)

        info = (
            'Sucesso', f'A viagem {nome_viagem_str} foi salva com sucesso!'
        )
        self.mw.aviso(info)

    def viagem_window_del(self):
        obj = 'del'
        WindowViagem(self.mw, self, obj)
