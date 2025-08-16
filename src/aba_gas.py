import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class AbaGas:
    def __init__(self, frame_pai, controller):
        self.frame_pai = frame_pai
        self.controller = controller
        self.cfg = self.controller.cfg_gas

        self.linhas_gas = []

    def criar_frame_aba(self):
        canvas = ttk.Canvas(self.frame_pai)
        scrollbar = ttk.Scrollbar(
            self.frame_pai, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.frame_gas = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.frame_gas, anchor="nw"
        )

        def centralizar_frame(event):
            canvas_width = event.width
            frame_width = self.frame_gas.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def redimensionar_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.frame_gas.bind("<Configure>", redimensionar_frame)
        canvas.bind("<Configure>", centralizar_frame)

    def criar_headers(self):
        headers = ["Data", "Destino", "Distânca", "Valor", ""]
        col_dados = len(headers)
        for col in range(5):
            self.frame_gas.grid_columnconfigure(col * 2, weight=0)

        for col, header in enumerate(headers):
            ttk.Label(
                self.frame_gas,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_dados - 1:
                ttk.Separator(
                    self.frame_gas,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

    def criar_linha(self, gas_viagem=None):
        if gas_viagem:
            data_inicial = gas_viagem['data']
            destino_inicial = gas_viagem['destino']
            dist_inicial = gas_viagem['dist']
        else:
            data_inicial = None
            destino_inicial = None
            dist_inicial = None

        linha = {}
        linha = {
            'data_var': data_inicial,
            'destino_var': destino_inicial,
            'dist_var': dist_inicial
        }
        row_num = len(self.linhas_gas) + 1

        self.criar_campo_data(linha, row_num)
        self.criar_campo_destino(linha, row_num)
        self.criar_campo_dist(linha, row_num)
        self.criar_campo_valor(linha, row_num)
        self.criar_removedor(linha, row_num)

        self.linhas_gas.append(linha)

    def criar_campo_data(self, linha, row_num):
        if linha['data_var']:
            data_inicial_datetime = datetime.strptime(
                linha['data_var'], '%d/%m/%Y'
            )
            data_entry = ttk.DateEntry(
                self.frame_gas,
                dateformat="%d/%m/%Y",
                startdate=data_inicial_datetime
            )

        else:
            data_entry = ttk.DateEntry(
                self.frame_gas,
                dateformat="%d/%m/%Y",
                startdate=datetime.now()
            )
        linha["data_entry"] = data_entry
        linha["data_var"] = data_entry.entry
        data_entry.grid(
            row=row_num,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

    def criar_campo_destino(self, linha, row_num):
        if linha['destino_var']:
            destino = Tk.StringVar(value=linha['destino_var'])
        else:
            destino = Tk.StringVar()

        destino_entry = ttk.Entry(
            self.frame_gas,
            textvariable=destino
        )
        destino_entry.grid(
            row=row_num,
            column=2,
            padx=5,
            pady=2,
            sticky='ew'
        )
        linha['destino_entry'] = destino_entry
        linha['destino_var'] = destino.get()

    def criar_campo_dist(self, linha, row_num):
        if linha['dist_var']:
            dist = Tk.StringVar(value=linha['dist_var'])
        else:
            dist = Tk.StringVar()

        frame_dist = ttk.Frame(
            self.frame_gas
        )
        linha['frame_dist'] = frame_dist
        frame_dist.grid(
            row=row_num,
            column=4,
        )
        dist_entry = ttk.Entry(
            frame_dist,
            textvariable=dist
        )
        linha['dist_entry'] = dist_entry
        km_label = ttk.Label(
            frame_dist,
            text='km'
        )
        linha['km_label'] = km_label
        dist_entry.pack(
            side=Tk.LEFT,
            fill=Tk.BOTH,
            expand=True,
            padx=5,
            pady=2
        )
        km_label.pack(
            side=Tk.LEFT
        )

        try:
            dist_str = dist.get()
            dist_float = float(dist_str.replace(',', '.').replace(' km', ''))
        except ValueError:
            dist_float = 0.0

        linha['dist'] = dist_float

    def criar_campo_valor(self, linha, row_num):
        consumo = self.cfg.get('consumo', 0.0)
        custo_gas = self.cfg.get('custo_gas', 0.0)
        dist = linha.get('dist', 0.0)
        valor = (custo_gas * dist) / (consumo)
        valor_entry = ttk.Label(
            self.frame_gas,
            text=f'R$ {valor}'
        )
        valor_entry.grid(
            row=row_num,
            column=6,
            padx=5,
            pady=2
        )
        linha['valor_entry'] = valor_entry

    def criar_removedor(self, linha, row_num):
        linha["removedor"] = ttk.Button(
            self.frame_gas,
            text="X",
            width=3,
            command=lambda: self.remover_linha(linha)
        )
        linha["removedor"].grid(row=row_num, column=8, padx=25, pady=2)

    def remover_linha(self, linha):
        for item in list(linha.values()):
            if isinstance(item, Tk.Widget):
                item.destroy()
        self.linhas_gas.remove(linha)
