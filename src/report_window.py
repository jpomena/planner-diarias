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

        self.CriarTabelaDespesas()
        self.PreencherTabelaDespesas()
        self.CriarTabelaTotais()
        self.PreencherTabelaTotais()

    def CriarTabelaDespesas(self):
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

    def PreencherTabelaDespesas(self):
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

    def CriarTabelaTotais(self):
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

    def PreencherTabelaTotais(self):
        lanche_total = 0.0
        manha_total = 0.0
        almoco_total = 0.0
        tarde_total = 0.0
        janta_total = 0.0
        for linha in self.linhas_despesas:
            tipo_str = linha['tipo_var'].get()
            valor_str = linha['valor_var'].get()
            valor_float = float(valor_str.replace('R$ ', '').replace(',', '.'))
            if tipo_str == "Lanche em Trajeto":
                lanche_total += valor_float
            elif tipo_str == 'Café da Manhã':
                manha_total += valor_float
            elif tipo_str == 'Almoço':
                almoco_total += valor_float
            elif tipo_str == 'Café da Tarde':
                tarde_total += valor_float
            elif tipo_str == 'Janta':
                janta_total += valor_float
        total_total = sum([
            lanche_total,
            manha_total,
            almoco_total,
            tarde_total,
            janta_total
        ])

        self.tabela_totais.insert(
            '',
            'end',
            values=(
                'Lanche em Trajeto', (f'R$ {lanche_total:.2f}').replace(
                    '.', ','
                )))
        self.tabela_totais.insert(
            '',
            'end',
            values=(
                'Café da Manhã', (f'R$ {manha_total:.2f}').replace('.', ',')
            ))
        self.tabela_totais.insert(
            '',
            'end',
            values=(
                'Almoço', (f'R$ {almoco_total:.2f}').replace('.', ',')
            ))
        self.tabela_totais.insert(
            '',
            'end',
            values=(
                'Café da Tarde', (f'R$ {tarde_total:.2f}').replace('.', ',')
            ))
        self.tabela_totais.insert(
            '',
            'end',
            values=(
                'Janta', (f'R$ {janta_total:.2f}').replace('.', ',')
            ))
        self.tabela_totais.insert(
            '',
            'end',
            values=(
                'Total', (f'R$ {total_total:.2f}').replace('.', ',')
            ))
