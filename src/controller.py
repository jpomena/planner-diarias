import tkinter as Tk
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
        self.linhas_despesas = []
        self.db = Database()
        self.mw = MainWindow(self)

        self.db.criar_tabelas()

        self.abrir_gui()

    def abrir_gui(self):
        self.nome_viagem = Tk.StringVar()
        self.mw.criar_frame_nome(self.nome_viagem)
        self.mw.criar_frame_controle()
        self.mw.criar_botoes_controle()
        self.mw.criar_botoes_sql()
        self.mw.criar_frame_despesas()
        self.mw.criar_headers()
        self.criar_linha()

    def criar_linha(self, despesa_viagem=None):
        if despesa_viagem:
            data_inicial = despesa_viagem['data']
            tipo_inicial = despesa_viagem['tipo']
            loc_inicial = despesa_viagem['loc']
        else:
            data_inicial = None
            tipo_inicial = None
            loc_inicial = None

        widgets_linha = {}
        row_num = len(self.linhas_despesas) + 1
        self.mw.criar_campo_data(widgets_linha, row_num, data_inicial)
        self.mw.criar_campo_tipo(widgets_linha, row_num, tipo_inicial)
        self.mw.criar_campo_loc(widgets_linha, row_num, loc_inicial)
        self.mw.criar_campo_valor(widgets_linha, row_num)
        self.atualizar_loc(widgets_linha, row_num)
        self.atualizar_valor(widgets_linha)
        self.mw.criar_removedor(widgets_linha, row_num)

        self.linhas_despesas.append(widgets_linha)

    def atualizar_loc(self, widgets_linha, row_num):
        tipo_str = widgets_linha["tipo_var"].get()
        if not tipo_str or tipo_str not in self.configs:
            self.mw.mostrar_localidade_irrelevante(widgets_linha, row_num)
            return
        pct_capitais = self.configs[tipo_str]['Capitais']
        pct_outras = self.configs[tipo_str]['Outras']

        if pct_capitais != pct_outras:
            self.mw.mostrar_localidade_relevante(widgets_linha, row_num)
        else:
            self.mw.mostrar_localidade_irrelevante(widgets_linha, row_num)

    def atualizar_valor(self, widgets_linha):
        tipo = widgets_linha["tipo_var"].get()
        loc = widgets_linha["loc_var"].get()
        pct = self.configs.get(tipo, {}).get(loc, 0.0)
        widgets_linha["valor_var"].set(
            f'R$ {(self.configs["Salário Mínimo"]/100)*pct:.2f}'.replace(
                ".", ","
            ))

    def remover_linha(self, widgets_linha):
        for widget in list(widgets_linha.values()):
            if isinstance(widget, Tk.Widget):
                widget.destroy()
        self.linhas_despesas.remove(widgets_linha)

        # Flake8 Reclamaria que minha reclamação é longa e.e
        # noqa: E501 Porque cargas d'água o tkinter não tá esvaziando isso de imediato? Gambiarra:
        self.mw.regridar_widgets(self.linhas_despesas)

    def abrir_configs(self):
        ConfigsWindow(self.mw, self, self.configs)

    def gerar_report(self):
        ReportWindow(self.mw, self.linhas_despesas)

    def atualizar_linhas(self):
        for i, linha in enumerate(self.linhas_despesas):
            self.atualizar_loc(linha, i+1)
            self.atualizar_valor(linha)

    def viagem_window_open(self):
        obj = 'open'
        WindowViagem(self.mw, self, obj, self.carregar_viagem)

    def carregar_viagem(self, nome_viagem):
        self.nome_viagem.set(nome_viagem)

        for linha in list(self.linhas_despesas):
            self.remover_linha(linha)

        despesas_viagem = self.db.get_despesas_por_nome(nome_viagem)
        for despesa in despesas_viagem:
            self.criar_linha(despesa)

        info = (
            'Sucesso', f'A viagem {nome_viagem} foi aberta com sucesso!'
        )
        self.mw.aviso(info)

    def fechar_viagem(self):
        for linha in list(self.linhas_despesas):
            self.remover_linha(linha)
        self.criar_linha()
        self.nome_viagem.set('')

    def salvar_viagem(self):
        despesas_viagem = []
        nome_viagem_str = self.nome_viagem.get()
        for linha in self.linhas_despesas:
            data_str = linha['data_var'].get()
            tipo_str = linha['tipo_var'].get()
            loc_str = linha['loc_var'].get()
            valor_str = linha['valor_var'].get()
            valor_float = float(
                valor_str.replace('R$ ', '').replace('.', '').replace(',', '.')
            )
            pct_capitais = self.configs[tipo_str]['Capitais']
            pct_outras = self.configs[tipo_str]['Outras']

            if pct_capitais == pct_outras:
                loc_str = 'Irrelevante'
            despesa = {
                'data': data_str,
                'tipo': tipo_str,
                'loc': loc_str,
                'valor': valor_float
            }
            despesas_viagem.append(despesa)
        self.db.add_viagem(nome_viagem_str)
        self.db.add_despesas(despesas_viagem, nome_viagem_str)

        info = (
            'Sucesso', f'A viagem {nome_viagem_str} foi salva com sucesso!'
        )
        self.mw.aviso(info)

    def viagem_window_del(self):
        obj = 'del'
        WindowViagem(self.mw, self, obj)
