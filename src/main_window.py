import tkinter as Tk
from tkinter import messagebox
import ttkbootstrap as ttk
from datetime import datetime


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

    def criar_frame_nome(self, nome_viagem):
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
            textvariable=nome_viagem
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
            command=self.controller.criar_linha
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
            command=self.controller.abrir_viagem_window
        )
        self.botao_fechar_viagem = ttk.Button(
            frame_sql,
            text='Fechar Viagem',
            command=self.controller.fechar_viagem
        )
        self.botao_add_viagem = ttk.Button(
            frame_sql,
            text='Salvar Viagem',
            command=self.controller.salvar_viagem
        )
        self.botao_del_viagem = ttk.Button(
            frame_sql,
            text='Apagar Viagem',
            command=self.controller.apagar_viagem
        )

        self.botao_abrir_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_fechar_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_add_viagem.pack(side=Tk.LEFT, padx=5, pady=5)
        self.botao_del_viagem.pack(side=Tk.LEFT, padx=5, pady=5)

    def criar_frame_despesas(self):
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
                self.controller.atualizar_loc(widgets_linha, row_num),
                self.controller.atualizar_valor(widgets_linha),
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
            row_num=row_num: self.controller.atualizar_valor(
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
            command=lambda: self.controller.remover_linha(widgets_linha),
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
