import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class AbaDespesas:
    def __init__(self, frame_pai, controller):
        self.frame_pai = frame_pai
        self.controller = controller
        self.configs = self.controller.configs_despesas
        self.tipos_despesa = self.controller.tipos_despesa

        self.linhas_despesas = []

    def criar_frame_aba(self):
        canvas = ttk.Canvas(self.frame_pai)
        scrollbar = ttk.Scrollbar(
            self.frame_pai, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.frame_despesas = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.frame_despesas, anchor="nw"
        )

        def centralizar_frame(event):
            canvas_width = event.width
            frame_width = self.frame_despesas.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def redimensionar_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.frame_despesas.bind("<Configure>", redimensionar_frame)
        canvas.bind("<Configure>", centralizar_frame)

        def rolar_mouse(event):
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")

        for widget in [canvas, self.frame_despesas]:
            widget.bind("<MouseWheel>", rolar_mouse)
            widget.bind("<Button-4>", rolar_mouse)
            widget.bind("<Button-5>", rolar_mouse)

    def criar_headers(self):
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
        self.criar_campo_data(
            widgets_linha, row_num, data_inicial
        )
        self.criar_campo_tipo(
            widgets_linha, row_num, tipo_inicial
        )
        self.criar_campo_loc(widgets_linha, row_num, loc_inicial)
        self.criar_campo_valor(widgets_linha, row_num)
        self.atualizar_loc(widgets_linha, row_num)
        self.atualizar_valor(widgets_linha)
        self.criar_removedor(widgets_linha, row_num)

        self.linhas_despesas.append(widgets_linha)

    def criar_campo_data(self, widgets_linha, row_num, data_inicial=None):
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

    def criar_campo_tipo(self, widgets_linha, row_num, tipo_inicial=None):
        if tipo_inicial:
            tipo_var = Tk.StringVar(value=tipo_inicial)
        else:
            tipo_var = Tk.StringVar()
        widgets_linha['tipo_var'] = tipo_var

        widgets_linha['tipo_combobox'] = ttk.Combobox(
            self.frame_despesas,
            textvariable=tipo_var,
            values=self.controller.tipos_despesa,
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
                self.atualizar_loc(widgets_linha, row_num),
                self.atualizar_valor(widgets_linha),
            ))

    def criar_campo_loc(self, widgets_linha, row_num, tipo_inicial=None):
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
            row_num=row_num: self.atualizar_valor(
                widgets_linha
            ))

    def mostrar_localidade_relevante(self, widgets_linha, row_num):
        loc_irrelevante = widgets_linha["loc_irrelevante"]
        loc_frame = widgets_linha["loc_frame"]

        loc_irrelevante.grid_remove()
        loc_frame.grid(row=row_num, column=4, padx=5, pady=2)

    def mostrar_localidade_irrelevante(self, widgets_linha, row_num):
        loc_irrelevante = widgets_linha["loc_irrelevante"]
        loc_frame = widgets_linha["loc_frame"]

        loc_frame.grid_remove()
        loc_irrelevante.grid(row=row_num, column=4, padx=5, pady=2)

    def criar_campo_valor(self, widgets_linha, row_num):
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

    def criar_removedor(self, widgets_linha, row_num):
        widgets_linha["removedor"] = ttk.Button(
            self.frame_despesas,
            text="X",
            width=3,
            command=lambda: self.remover_linha(widgets_linha),
        )
        widgets_linha["removedor"].grid(row=row_num, column=8, padx=25, pady=2)

    def regridar_widgets(self, linhas_despesas):
        for index, linha in enumerate(linhas_despesas):
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

    def atualizar_loc(self, widgets_linha, row_num):
        tipo_str = widgets_linha["tipo_var"].get()
        if not tipo_str or tipo_str not in self.configs:
            self.mostrar_localidade_irrelevante(widgets_linha, row_num)
            return
        pct_capitais = self.configs[tipo_str]['Capitais']
        pct_outras = self.configs[tipo_str]['Outras']

        if pct_capitais != pct_outras:
            self.mostrar_localidade_relevante(widgets_linha, row_num)
        else:
            self.mostrar_localidade_irrelevante(widgets_linha, row_num)

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
        self.regridar_widgets(self.linhas_despesas)

    def atualizar_desps(self):
        for i, linha in enumerate(self.linhas_despesas):
            self.atualizar_loc(linha, i+1)
            self.atualizar_valor(linha)

    def carregar_despesas(self, despesas_viagem):
        for despesa in despesas_viagem:
            self.criar_linha(despesa)

    def fechar_despesas(self, obj=None):
        for linha in list(self.linhas_despesas):
            self.remover_linha(linha)
        if not obj:
            self.criar_linha()

    def dados_despesas(self):
        despesas_viagem = []
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
        return despesas_viagem
