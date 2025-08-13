import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk
from datetime import datetime
from .configs_window import ConfigsWindow
from .report_window import ReportWindow
from .database import Database
from .viagens_window import AbrirWindow
from .viagens_window import ApagarWindow


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title("Planner de Diárias")
        self.geometry("750x900")
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
        self.db = Database()

        self.db.CriarTabelas()
        self.CriarFrameNome()
        self.CriarFrameControle()
        self.CriarBotoesControle()
        self.CriarBotoesSQL()
        self.CriarFrameDespesas()
        self.CriarHeaders()
        self.CriarLinha()

    def CriarFrameNome(self):
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

        self.nome_viagem = Tk.StringVar()
        entry_nome = ttk.Entry(
            self.frame_nome,
            textvariable=self.nome_viagem
        )
        entry_nome.pack(fill=Tk.X, expand=True, padx=5, pady=2)

    def CriarFrameControle(self):
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

    def CriarBotoesControle(self):
        frame_botoes = ttk.Frame(self.frame_controle)
        frame_botoes.pack(expand=True, anchor='center')

        self.botao_add_linha = ttk.Button(
            frame_botoes,
            text="Adicionar Linha",
            command=self.CriarLinha
        )
        self.botao_report = ttk.Button(
            frame_botoes,
            text="Gerar Relatório",
            command=self.GerarReport
        )
        self.botao_configs = ttk.Button(
            frame_botoes,
            text="Configurações",
            command=self.AbrirConfigs
        )

        self.botao_add_linha.pack(side=Tk.LEFT, padx=5, pady=4)
        self.botao_report.pack(side=Tk.LEFT, padx=5, pady=4)
        self.botao_configs.pack(side=Tk.LEFT, padx=5, pady=4)

    def CriarBotoesSQL(self):
        frame_sql = ttk.Frame(
            self.frame_0
        )
        frame_sql.pack(side=Tk.BOTTOM, anchor='s', padx=5, pady=2)

        self.botao_abrir_viagem = ttk.Button(
            frame_sql,
            text='Abrir Viagem',
            command=self.AbrirViagemWindow
        )
        self.botao_fechar_viagem = ttk.Button(
            frame_sql,
            text='Fechar Viagem',
            command=self.FecharViagem
        )
        self.botao_add_viagem = ttk.Button(
            frame_sql,
            text='Salvar Viagem',
            command=self.SalvarViagem
        )
        self.botao_del_viagem = ttk.Button(
            frame_sql,
            text='Apagar Viagem',
            command=self.ApagarViagem
        )

        self.botao_abrir_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_fechar_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_add_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_del_viagem.pack(side=Tk.LEFT, padx=5, pady=5)

    def CriarFrameDespesas(self):
        container = ttk.LabelFrame(
            self.frame_0, text="Despesas", padding=5
        )
        container.pack(fill=Tk.BOTH, expand=True, anchor='n')

        canvas = ttk.Canvas(container)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.frame_despesas = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.frame_despesas, anchor="nw"
        )

        def center_frame(event):
            canvas_width = event.width
            frame_width = self.frame_despesas.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.frame_despesas.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", center_frame)

        def on_mouse_wheel(event):
            # A direção da rolagem pode variar entre sistemas operacionais
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")

        for widget in [canvas, self.frame_despesas]:
            widget.bind("<MouseWheel>", on_mouse_wheel)
            widget.bind("<Button-4>", on_mouse_wheel)
            widget.bind("<Button-5>", on_mouse_wheel)

    def CriarHeaders(self):
        headers = ["Data", "Tipo", "Localidade", "Valor", ""]
        col_dados = len(headers)
        for col in range(5):
            self.frame_despesas.grid_columnconfigure(col * 2, weight=0)

        for col, header in enumerate(headers):
            ttk.Label(
                self.frame_despesas,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_dados - 1:
                ttk.Separator(
                    self.frame_despesas,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

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
        self.CriarCampoData(widgets_linha, row_num, data_inicial)
        self.CriarCampoTipo(widgets_linha, row_num, tipo_inicial)
        self.CriarCampoLocalidade(widgets_linha, row_num, loc_inicial)
        self.CriarCampoValor(widgets_linha, row_num)
        self.MostrarLocalidade(widgets_linha, row_num)
        self.AtualizarValor(widgets_linha)
        self.CriarRemovedor(widgets_linha, row_num)

        self.linhas_despesas.append(widgets_linha)

    def CriarCampoData(self, widgets_linha, row_num, data_inicial=None):
        if data_inicial:
            data_inicial_datetime = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_entry = ttk.DateEntry(
                self.frame_despesas,
                dateformat="%d/%m/%Y",
                startdate=data_inicial_datetime
            )

        else:
            data_entry = ttk.DateEntry(
                self.frame_despesas,
                dateformat="%d/%m/%Y",
                startdate=datetime.now()
            )
        widgets_linha["data_entry"] = data_entry
        widgets_linha["data_var"] = data_entry.entry
        data_entry.grid(
            row=row_num,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

    def CriarCampoTipo(self, widgets_linha, row_num, tipo_inicial=None):
        if tipo_inicial:
            tipo_var = Tk.StringVar(value=tipo_inicial)
        else:
            tipo_var = Tk.StringVar()
        widgets_linha['tipo_var'] = tipo_var

        widgets_linha['tipo_combobox'] = ttk.Combobox(
            self.frame_despesas,
            textvariable=tipo_var,
            values=self.tipos_despesa,
            state="readonly",
        )
        widgets_linha["tipo_combobox"].grid(
            row=row_num,
            column=2,
            padx=5,
            pady=2,
            sticky="ew",
        )

        widgets_linha["tipo_combobox"].bind(
            "<<ComboboxSelected>>",
            lambda event, widgets_linha=widgets_linha, row_num=row_num: (
                self.MostrarLocalidade(widgets_linha, row_num),
                self.AtualizarValor(widgets_linha),
            ))

    def CriarCampoLocalidade(self, widgets_linha, row_num, tipo_inicial=None):
        if tipo_inicial:
            loc_var = Tk.StringVar(value=tipo_inicial)
        else:
            loc_var = Tk.StringVar(value='Irrelevante')
        loc_frame = ttk.Frame(self.frame_despesas)
        widgets_linha["loc_frame"] = loc_frame
        widgets_linha["loc_irrelevante"] = ttk.Label(
            self.frame_despesas,
            text="Irrelevante",
            anchor="center",
            width="20"
        )
        ttk.Radiobutton(
            loc_frame, text="Capitais", value="Capitais", variable=loc_var
        ).pack(side=Tk.LEFT, expand=True, fill=Tk.X, padx=5, pady=2)
        ttk.Radiobutton(
            loc_frame, text="Outras", value="Outras", variable=loc_var
        ).pack(side=Tk.LEFT, expand=True, fill=Tk.X, padx=5, pady=2)

        widgets_linha["loc_var"] = loc_var
        loc_var.trace_add(
            "write",
            lambda *args,
            widgets_linha=widgets_linha,
            row_num=row_num: self.AtualizarValor(
                widgets_linha
            ))

    def MostrarLocalidade(self, widgets_linha, row_num):
        loc_irrelevante = widgets_linha["loc_irrelevante"]
        loc_frame = widgets_linha["loc_frame"]

        if (
            widgets_linha["tipo_var"].get() == "Janta"
            or widgets_linha["tipo_var"].get() == "Almoço"
        ):
            loc_irrelevante.grid_remove()
            loc_frame.grid(row=row_num, column=4, padx=5, pady=2)
        else:
            loc_frame.grid_remove()
            loc_irrelevante.grid(row=row_num, column=4, padx=5, pady=2)

    def CriarCampoValor(self, widgets_linha, row_num):
        valor_var = Tk.StringVar(value="R$ 0,00")
        widgets_linha["valor_var"] = valor_var

        widgets_linha["valor_label"] = ttk.Label(
            self.frame_despesas,
            textvariable=widgets_linha["valor_var"],
            anchor="e"
        )
        widgets_linha["valor_label"].grid(
            row=row_num, column=6, padx=5, pady=2, sticky="ew"
        )

    def AtualizarValor(self, widgets_linha):
        tipo = widgets_linha["tipo_var"].get()
        loc = widgets_linha["loc_var"].get()
        pct = self.configs.get(tipo, {}).get(loc, 0.0)
        widgets_linha["valor_var"].set(
            f'R$ {(self.configs["Salário Mínimo"]/100)*pct:.2f}'.replace(
                ".", ","
            ))

    def CriarRemovedor(self, widgets_linha, row_num):
        widgets_linha["removedor"] = ttk.Button(
            self.frame_despesas,
            text="X",
            width=3,
            command=lambda: self.RemoverLinha(widgets_linha),
        )
        widgets_linha["removedor"].grid(row=row_num, column=8, padx=25, pady=2)

    def RemoverLinha(self, widgets_linha):
        for widget in list(widgets_linha.values()):
            if isinstance(widget, Tk.Widget):
                widget.destroy()
        self.linhas_despesas.remove(widgets_linha)


# Porque cargas d'água o tkinter não tá esvaziando isso de imediato? Gambiarra:
        for index, linha in enumerate(self.linhas_despesas):
            row_num = index + 1
            linha['data_entry'].grid(
                row=row_num,
                column=0,
                padx=5,
                pady=2,
                sticky="ew"
            )
            linha['tipo_combobox'].grid(
                row=row_num,
                column=2,
                padx=5,
                pady=2,
                sticky="ew"
            )

            if linha['tipo_var'].get() in ["Almoço", "Janta"]:
                linha['loc_irrelevante'].grid_remove()
                linha['loc_frame'].grid(
                    row=row_num,
                    column=4,
                    padx=5,
                    pady=2
                )
            else:
                linha['loc_frame'].grid_remove()
                linha['loc_irrelevante'].grid(
                    row=row_num,
                    column=4,
                    padx=5,
                    pady=2
                )

            linha['valor_label'].grid(
                row=row_num,
                column=6,
                padx=5,
                pady=2,
                sticky="ew"
            )
            linha['removedor'].grid(
                row=row_num,
                column=8,
                padx=25,
                pady=2
            )

    def AbrirConfigs(self):
        ConfigsWindow(self, self.configs)

    def GerarReport(self):
        ReportWindow(self, self.linhas_despesas)

    def AtualizarLinhas(self):
        for linha in self.linhas_despesas:
            self.AtualizarValor(linha)

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

        messagebox.showinfo(
            'Sucesso', f'A viagem {nome_viagem_str} foi salva com sucesso!'
        )

    def AbrirViagemWindow(self):
        AbrirWindow(self, self.CarregarViagem)

    def CarregarViagem(self, nome_viagem):
        self.nome_viagem.set(nome_viagem)

        for linha in list(self.linhas_despesas):
            self.RemoverLinha(linha)

        despesas_viagem = self.db.ObterDespesasPorNomeViagem(nome_viagem)
        for despesa in despesas_viagem:
            self.CriarLinha(despesa)

        messagebox.showinfo(
            'Sucesso', f'A viagem {nome_viagem} foi aberta com sucesso!'
        )

    def FecharViagem(self):
        for linha in list(self.linhas_despesas):
            self.RemoverLinha(linha)
        self.CriarLinha()
        self.nome_viagem.set('')

    def ApagarViagem(self):
        ApagarWindow(self)
