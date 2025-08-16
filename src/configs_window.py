import tkinter as Tk
import ttkbootstrap as ttk


class ConfigsWindow(Tk.Toplevel):
    def __init__(self, master, controller, tipo_config):
        super().__init__(master)
        self.mw = master
        self.controller = controller
        self.configs_despesas = self.controller.configs_despesas
        self.configs_gas = self.controller.configs_gas
        self.tipos_despesa = list(self.configs_despesas.keys())
        self.validando_decimal = False
        self.validando_moeda = False

        self.title("Configurações")
        if tipo_config == 'despesas':
            self.geometry("400x400")
        elif tipo_config == 'gas':
            self.geometry('400x150')
        self.transient(master)
        self.grab_set()

        self.povoar_configs(tipo_config)

        self.protocol('WM_DELETE_WINDOW', self.fechar)

    def povoar_configs(self, tipo_config):
        if tipo_config == 'despesas':
            self.criar_frame_configs_despesas()
            self.despesas_criar_labels()
            self.despesas_criar_entry_salario()
            self.despesas_criar_entry_porcentagens('Capitais', 2)
            self.despesas_criar_entry_porcentagens('Outras', 4)

        if tipo_config == 'gas':
            self.criar_frame_configs_gas()
            self.criar_entry_configs_gas_custo()
            self.criar_entry_configs_gas_consumo()

    def criar_frame_configs_despesas(self):
        self.frame_configs_despesas = ttk.Frame(
            self,
            padding=10
        )
        self.frame_configs_despesas.pack(padx=5, pady=2)
        self.frame_pct_despesas = ttk.LabelFrame(
            self.frame_configs_despesas,
            text='Percentuais de Reembolso',
            padding=10
        )
        self.frame_pct_despesas.grid(
            row=1,
            column=0,
            columnspan=5,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def despesas_criar_labels(self):
        for index, config in enumerate(self.tipos_despesa[1:], 1):
            self.frame_pct_despesas.grid_rowconfigure(
                index, weight=0
            )
            ttk.Label(
                self.frame_pct_despesas,
                text=config,
                justify="right"
            ).grid(row=index+1, column=0, padx=5, pady=2)

        for col in range(6):
            self.frame_configs_despesas.grid_columnconfigure(
                col, weight=0
            )
            self.frame_configs_despesas.grid_columnconfigure(
                1, minsize=0
            )

        for index, tipo in enumerate(list(['Capitais', 'Outras'])):
            ttk.Label(
                self.frame_pct_despesas,
                text=tipo,
                justify='center',
            ).grid(row=1, column=(index+1)*2, padx=5, pady=2)

    def formatar_moeda(self, numero):
        formatted = f'R$ {numero:,.2f}'
        return formatted.replace(',', '#').replace('.', ',').replace('#', '.')

    def validar_moeda(self, valor, dict_cfg, dict_key, *trace_info):
        if self.validando_moeda:
            return
        self.validando_moeda = True

        try:
            valor_str = valor.get()
            valor_num = ''.join(filter(str.isdigit, valor_str))

            if not valor_num:
                valor_float = 0.0
            else:
                valor_float = int(valor_num)/100

            valor.set(self.formatar_moeda(valor_float))
            dict_cfg[dict_key] = valor_float

        finally:
            self.validando_moeda = False

    def despesas_criar_entry_salario(self):
        sm_frame = ttk.LabelFrame(
            self.frame_configs_despesas,
            text='Salário Mínimo'
        )
        sm_frame.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=5,
            pady=2,
            sticky='ew'
        )
        sm_var = Tk.StringVar(
            value=self.formatar_moeda(
                self.configs_despesas['Salário Mínimo']
            ))
        sm_var.trace_add(
            'write', self._callback_validar_moeda(
                sm_var, self.configs_despesas, 'Salário Mínimo'
                ))

        entry_sm = ttk.Entry(
            sm_frame,
            textvariable=sm_var,
            validate='all',
            validatecommand=(
                self.register(self.validar_append_entries),
                '%d',
                '%P',
                '%i',
                '%S'
            ),
            justify='right'
        )

        entry_sm.pack(fill=Tk.X, expand=True, padx=5, pady=2)
        entry_sm.bind("<Button-1>", self.empurrar_caret)
        entry_sm.bind("<Key>", self.empurrar_caret)

    def formatar_decimal(self, numero):
        return f'{numero:.1f}'.replace('.', ',')

    def validar_decimal(self, num, dict_cfg, dict_key, loc_despesa=None, *t):
        if self.validando_decimal:
            return

        self.validando_decimal = True
        numero_str = num.get()
        numero_cru = ''.join(filter(str.isdigit, numero_str))

        if not numero_cru:
            numero_float = 0.0
        else:
            numero_float = int(numero_cru)/10
        if numero_float > 100.0:
            numero_float = 100.0

        if dict_cfg == self.configs_despesas:
            dict_cfg[dict_key][loc_despesa] = numero_float
            num.set(self.formatar_decimal(numero_float))

            pct_cap = dict_cfg[dict_key].get('Capitais', 0.0)
            pct_outras = dict_cfg[dict_key].get('Outras', 0.0)
            if pct_cap == pct_outras:
                self.configs_despesas[dict_key]['Irrelevante'] = pct_cap
            else:
                self.configs_despesas[dict_key]['Irrelevante'] = 0.0
        elif dict_cfg == self.configs_gas:
            dict_cfg[dict_key] = numero_float
            num.set(self.formatar_decimal(numero_float))

        self.validando_decimal = False

    def despesas_criar_entry_porcentagens(self, loc, coluna):
        for index, tipo in enumerate(list(self.configs_despesas.keys())[1:]):
            pct_var = Tk.StringVar(
                value=self.formatar_decimal(
                    self.configs_despesas[tipo][loc]
                ))

            pct_var.trace_add(
                'write',
                lambda *args,
                v=pct_var,
                d=self.configs_despesas,
                t=tipo,
                c=loc: self.validar_decimal(
                    v, d, t, c, *args
                ))

            frame_entry = ttk.Frame(self.frame_pct_despesas)
            frame_entry.grid(
                row=index+2,
                column=coluna,
                padx=5,
                pady=2,
                sticky='ew'
            )

            pct_entry = ttk.Entry(
                frame_entry,
                textvariable=pct_var,
                width=5,
                justify='right',
                validate='all',
                validatecommand=(
                    self.register(self.validar_append_entries),
                    '%d',
                    '%P',
                    '%i',
                    '%S'
                ))

            pct_entry.pack(side=Tk.LEFT, padx=(0, 2))
            pct_entry.bind("<Button-1>", self.empurrar_caret)
            pct_entry.bind("<Key>", self.empurrar_caret)

            ttk.Label(
                frame_entry,
                text='%',
                justify='left'
            ).pack(side=Tk.LEFT)

    def validar_append_entries(self, tipo_acao, valor_after, index, substring):
        if tipo_acao != '1':
            return True

        if int(index) >= len(valor_after) - len(substring):
            return True

        return False

    def empurrar_caret(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def fechar(self):
        self.mw.atualizar_abas()
        self.destroy()

    def criar_frame_configs_gas(self):
        self.frame_configs_gas = ttk.Frame(
            self,
            padding=10
        )
        self.frame_configs_gas.pack(fill=Tk.X, expand=True, anchor='center')

    def criar_entry_configs_gas_custo(self):
        valor_str = Tk.StringVar(
            value=self.formatar_moeda(self.configs_gas['custo_gas'])
        )
        valor_str.trace_add(
            'write', self._callback_validar_moeda(
                valor_str, self.configs_gas, 'custo_gas'
            ))

        frame_entry = ttk.LabelFrame(
            self.frame_configs_gas,
            text='Preço do combustível por litro',
        )
        frame_entry.pack(
            side=Tk.TOP, fill=Tk.BOTH, expand=True, padx=5, pady=2
        )
        config_entry = ttk.Entry(
            frame_entry,
            textvariable=valor_str,
            validate='all',
            validatecommand=(
                self.register(self.validar_append_entries),
                '%d',
                '%P',
                '%i',
                '%S'
            ), justify='right')
        config_entry.pack(fill=Tk.X, expand=True, padx=5, pady=2)
        config_entry.bind("<Button-1>", self.empurrar_caret)
        config_entry.bind("<Key>", self.empurrar_caret)

    def criar_entry_configs_gas_consumo(self):
        valor_str = Tk.StringVar(
            value=self.formatar_decimal(self.configs_gas['consumo'])
        )
        valor_str.trace_add(
            'write', (
                lambda *args,
                v=valor_str,
                d=self.configs_gas,
                k='custo_gas',
                loc=None:
                    self.validar_decimal(v, d, k, loc, *args)
            ))

        frame_entry = ttk.LabelFrame(
            self.frame_configs_gas,
            text='Rendimento do veículo (km/L)',
        )
        frame_entry.pack(
            side=Tk.TOP, fill=Tk.BOTH, expand=True, padx=5, pady=2
        )
        config_entry = ttk.Entry(
            frame_entry,
            textvariable=valor_str,
            validate='all',
            validatecommand=(
                self.register(self.validar_append_entries),
                '%d',
                '%P',
                '%i',
                '%S'
            ), justify='right')
        config_entry.pack(fill=Tk.X, expand=True, padx=5, pady=2)
        config_entry.bind("<Button-1>", self.empurrar_caret)
        config_entry.bind("<Key>", self.empurrar_caret)

    def _callback_validar_moeda(self, valor, dict_cfg, dict_key):
        return lambda *args: self.validar_moeda(
            valor, dict_cfg, dict_key, *args
        )
