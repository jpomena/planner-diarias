import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class AbaGas:
    def __init__(self, frame_pai, controller):
        self.frame_pai = frame_pai
        self.controller = controller
        self.cfg = self.controller.cfg_gas
        self.validando_dist = False

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
        headers = ["Data", "Trajeto", "Distância", "Valor", ""]
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

        linha = {
            'data_gas': data_inicial,
            'destino_gas': destino_inicial,
            'dist_gas': dist_inicial
        }
        row_num = len(self.linhas_gas) + 1

        self.criar_campo_data(linha, row_num)
        self.criar_campo_destino(linha, row_num)
        self.criar_campo_dist(linha, row_num)
        self.criar_campo_valor(linha, row_num)
        self.criar_removedor(linha, row_num)
        self.atualizar_valor(linha)

        self.linhas_gas.append(linha)

    def criar_campo_data(self, linha, row_num):
        if linha['data_gas']:
            data_inicial_datetime = datetime.strptime(
                linha['data_gas'], '%d/%m/%Y'
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
        linha["data_gas"] = data_entry.entry
        data_entry.grid(
            row=row_num,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

    def criar_campo_destino(self, linha, row_num):
        if not linha['destino_gas']:
            linha['destino_gas'] = Tk.StringVar()
        else:
            linha['destino_gas'] = Tk.StringVar(value=linha['destino_gas'])

        destino_entry = ttk.Entry(
            self.frame_gas,
            textvariable=linha['destino_gas']
        )
        destino_entry.grid(
            row=row_num,
            column=2,
            padx=5,
            pady=2,
            sticky='ew'
        )
        linha['destino_entry'] = destino_entry

    def criar_campo_dist(self, linha, row_num):
        if not linha['dist_gas']:
            linha['dist_gas'] = Tk.StringVar()
        else:
            linha['dist_gas'] = Tk.StringVar(value=linha['dist_gas'])
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
            textvariable=linha['dist_gas'],
            justify='right'
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
        linha['dist_gas'].trace_add(
            'write',
            lambda *args, lin=linha: self.validar_dist(lin, *args)
        )
        linha['dist_entry'].bind('<Key>', self.empurrar_caret)
        linha['dist_entry'].bind('<Button-1>', self.empurrar_caret)

    def criar_campo_valor(self, linha, row_num):
        valor = Tk.StringVar(value='R$ 0,00')
        linha['valor_gas'] = valor
        valor_entry = ttk.Label(
            self.frame_gas,
            textvariable=linha['valor_gas'],
            justify='right'
        )
        valor_entry.grid(
            row=row_num,
            column=6,
            padx=5,
            pady=2
        )
        linha['valor_entry'] = valor_entry

    def criar_removedor(self, linha, row_num):
        linha['removedor'] = ttk.Button(
            self.frame_gas,
            text='X',
            width=3,
            command=lambda: self.remover_linha(linha)
        )
        linha['removedor'].grid(row=row_num, column=8, padx=25, pady=2)

    def remover_linha(self, linha):
        for item in list(linha.values()):
            if isinstance(item, Tk.Widget):
                item.destroy()
        self.linhas_gas.remove(linha)

    def atualizar_valor(self, linha):
        try:
            dist_str = linha.get('dist_gas').get()
            dist_float = float(dist_str.replace(',', '.'))
        except ValueError:
            dist_float = 0.0
        consumo = self.cfg.get('consumo', 0.0)
        custo_gas = self.cfg.get('custo_gas', 0.0)
        valor = (custo_gas * dist_float) / (consumo)
        linha['valor_gas'].set(f'R$ {valor:.2f}'.replace('.', ','))

    def atualizar_gas(self):
        for linha in self.linhas_gas:
            self.atualizar_valor(linha)

    def carregar_gas(self, gas_viagem):
        for linha in gas_viagem:
            self.criar_linha(linha)

    def formatar_dist(self, num_float,):
        return f'{num_float:.1f}'.replace('.', ',')

    def validar_dist(self, linha, *args):
        if self.validando_dist:
            return
        self.validando_dist = True

        valor_str = linha['dist_gas'].get()
        valor_cru = "".join(filter(str.isdigit, valor_str))
        if not valor_cru:
            valor_float = 0.0
        else:
            valor_float = int(valor_cru) / 10

        linha['dist_gas'].set(self.formatar_dist(valor_float))
        self.atualizar_valor(linha)

        self.validando_dist = False

    def empurrar_caret(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def get_dados_gas(self):
        dados_gas = []
        for linha in self.linhas_gas:
            data_str = linha['data_gas'].get()
            try:
                tipo_str = linha['destino_gas'].get()
            except AttributeError:
                tipo_str = linha['destino_gas']
            loc_str = linha['dist_gas'].get()
            valor_cru = linha['valor_gas'].get()
            valor_str = (
                valor_cru
                .replace('R$ ', '')
                .replace('.', '')
                .replace(',', '.')
            )
            valor_float = float(valor_str)

            gas = {
                'data_gas': data_str,
                'destino_gas': tipo_str,
                'dist_gas': loc_str,
                'valor_gas': valor_float
            }
            dados_gas.append(gas)
        return dados_gas

    def fechar_gas(self, obj=None):
        for linha in list(self.linhas_gas):
            self.remover_linha(linha)
        if not obj:
            self.criar_linha()
