import tkinter as Tk
import ttkbootstrap as ttk


class ReportWindow(Tk.Toplevel):
    def __init__(self, master, linhas_despesas):
        super().__init__(master)
        self.master = master
        self.title('Resumo')
        self.geometry('600x600')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.linhas_despesas = linhas_despesas

        self.frame_resumo = ttk.Frame(
            self
        )
        self.frame_resumo.pack(fill=Tk.BOTH, expand=True, padx=5, pady=2)

        self.criar_tabela_despesas()
        self.preencher_tabela_despesas()
        self.criar_tabela_totais()
        self.preencher_tabela_totais()

    def criar_tabela_despesas(self):
        columns_ids = ['data', 'tipo', 'loc', 'val']
        headers = {
            'data': 'Data',
            'tipo': 'Tipo de Despesa',
            'loc': 'Localidade',
            'val': 'Valor'
        }

        frame_tabela = ttk.LabelFrame(
            self.frame_resumo,
            text='Despesas',
            padding=10
        )
        frame_tabela.pack(side=Tk.TOP, fill=Tk.BOTH, padx=5, pady=5)

        self.tabela_despesas = ttk.Treeview(
            frame_tabela,
            columns=columns_ids,
            show='headings'
        )
        self.tabela_despesas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

        for col in columns_ids:
            self.tabela_despesas.heading(f'{col}', text=f'{headers[col]}')
            self.tabela_despesas.column(col, width=75, anchor='center')

        scroll_despesas = ttk.Scrollbar(
            frame_tabela,
            orient=Tk.VERTICAL,
            command=self.tabela_despesas.yview
        )
        scroll_despesas.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.tabela_despesas.configure(yscrollcommand=scroll_despesas.set)

    def preencher_tabela_despesas(self):
        for linha in self.linhas_despesas:
            data_str = linha['data_var'].get()
            tipo_str = linha['tipo_var'].get()
            loc_str = linha['loc_var'].get()
            valor_float = linha['valor_var'].get()
            if tipo_str != 'Almoço' and tipo_str != 'Janta':
                loc_str = 'Irrelevante'
            self.tabela_despesas.insert(
                '',
                'end',
                values=(
                    data_str,
                    tipo_str,
                    loc_str,
                    valor_float
                ))

    def criar_tabela_totais(self):
        frame_totais = ttk.LabelFrame(
            self.frame_resumo,
            text='Totais',
            padding=10
        )
        frame_totais.pack(
            side=Tk.TOP,
            fill=Tk.BOTH,
            expand=True,
            padx=5,
            pady=2
            )

        columns_ids = ('tipos', 'total')
        headers = {
            'tipos': 'Tipo de Despesa',
            'total': 'Total'
        }
        self.tabela_totais = ttk.Treeview(
            frame_totais,
            columns=columns_ids,
            show='headings'
        )
        self.tabela_totais.pack(
            fill=Tk.BOTH,
            expand=True,
            padx=5,
            pady=2
            )
        for col in columns_ids:
            self.tabela_totais.heading(f'{col}', text=f'{headers[col]}')
            self.tabela_totais.column(col, width=150, anchor='center')

    def preencher_tabela_totais(self):
        tipos_despesa = [
            'Lanche em Trajeto',
            'Café da Manhã',
            'Almoço',
            'Café da Tarde',
            'Janta',
            'Total'
        ]
        totais_despesas = {}

        for tipo in tipos_despesa:
            totais_despesas[f'{tipo}'] = 0.0

        for linha in self.linhas_despesas:
            tipo_str = linha['tipo_var'].get()
            valor_str = linha['valor_var'].get()
            valor_float = float(valor_str.replace('R$ ', '').replace(',', '.'))
            totais_despesas[f'{tipo_str}'] += valor_float
            totais_despesas['Total'] += valor_float

        for tipo in tipos_despesa:
            self.tabela_totais.insert(
                '',
                'end',
                values=(
                    f'{tipo}', (f'R$ {totais_despesas[tipo]:.2f}').replace(
                        '.', ','
                    )))
