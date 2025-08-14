import tkinter as Tk
from .database import Database
from .main_window import MainWindow
from .configs_window import ConfigsWindow
from .report_window import ReportWindow
from .viagens_window import AbrirWindow
from .viagens_window import ApagarWindow


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

        self.db.CriarTabelas()

        self.AbrirGUI()

    def AbrirGUI(self):
        self.nome_viagem = Tk.StringVar()
        self.mw.CriarFrameNome(self.nome_viagem)
        self.mw.CriarFrameControle()
        self.mw.CriarBotoesControle()
        self.mw.CriarBotoesSQL()
        self.mw.CriarFrameDespesas()
        self.mw.CriarHeaders()
        self.CriarLinha()

    def CriarLinha(self, despesa_viagem=None):
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
        self.mw.CriarCampoData(widgets_linha, row_num, data_inicial)
        self.mw.CriarCampoTipo(widgets_linha, row_num, tipo_inicial)
        self.mw.CriarCampoLocalidade(widgets_linha, row_num, loc_inicial)
        self.mw.CriarCampoValor(widgets_linha, row_num)
        self.MostrarLocalidade(widgets_linha, row_num)
        self.AtualizarValor(widgets_linha)
        self.mw.CriarRemovedor(widgets_linha, row_num)

        self.linhas_despesas.append(widgets_linha)

    def MostrarLocalidade(self, widgets_linha, row_num):
        tipo_var_str = widgets_linha["tipo_var"]
        if (tipo_var_str == "Janta" or tipo_var_str == "Almoço"):
            self.mw.MostrarLocalidadeRelevante(widgets_linha, row_num)
        else:
            self.mw.MostrarLocalidadeIrrelevante(widgets_linha, row_num)

    def AtualizarValor(self, widgets_linha):
        tipo = widgets_linha["tipo_var"].get()
        loc = widgets_linha["loc_var"].get()
        pct = self.configs.get(tipo, {}).get(loc, 0.0)
        widgets_linha["valor_var"].set(
            f'R$ {(self.configs["Salário Mínimo"]/100)*pct:.2f}'.replace(
                ".", ","
            ))

    def RemoverLinha(self, widgets_linha):
        for widget in list(widgets_linha.values()):
            if isinstance(widget, Tk.Widget):
                widget.destroy()
        self.linhas_despesas.remove(widgets_linha)

        # Flake8 Reclamaria que minha reclamação é longa e.e
        # noqa: E501 Porque cargas d'água o tkinter não tá esvaziando isso de imediato? Gambiarra:
        self.mw.RegridarWidgets(self.linhas_despesas)

    def AbrirConfigs(self):
        ConfigsWindow(self.mw, self, self.configs)

    def GerarReport(self):
        ReportWindow(self.mw, self.linhas_despesas)

    def AtualizarLinhas(self):
        for linha in self.linhas_despesas:
            self.AtualizarValor(linha)

    def AbrirViagemWindow(self):
        AbrirWindow(self.mw, self, self.CarregarViagem)

    def CarregarViagem(self, nome_viagem):
        self.nome_viagem.set(nome_viagem)

        for linha in list(self.linhas_despesas):
            self.RemoverLinha(linha)

        despesas_viagem = self.db.ObterDespesasPorNomeViagem(nome_viagem)
        for despesa in despesas_viagem:
            self.CriarLinha(despesa)

        info = (
            'Sucesso', f'A viagem {nome_viagem} foi aberta com sucesso!'
        )
        self.mw.Aviso(info)

    def FecharViagem(self):
        for linha in list(self.linhas_despesas):
            self.RemoverLinha(linha)
        self.CriarLinha()
        self.nome_viagem.set('')

    def SalvarViagem(self):
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
            if tipo_str != 'Almoço' and tipo_str != 'Janta':
                loc_str = 'Irrelevante'
            despesa = {
                'data': data_str,
                'tipo': tipo_str,
                'loc': loc_str,
                'valor': valor_float
            }
            despesas_viagem.append(despesa)
        self.db.AdicionarViagem(nome_viagem_str)
        self.db.AdicionarDespesas(despesas_viagem, nome_viagem_str)

        info = (
            'Sucesso', f'A viagem {nome_viagem_str} foi salva com sucesso!'
        )
        self.mw.Aviso(info)

    def ApagarViagem(self):
        ApagarWindow(self.mw, self)
