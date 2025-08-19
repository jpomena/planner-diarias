import tkinter as Tk
import ttkbootstrap as ttk


class ConfigWindow(Tk.Toplevel):
    def __init__(self, master, controller, current_tab):
        super().__init__(master)
        self.main_window = master
        self.controller = controller
        self.expenses_config = self.controller.expenses_config
        self.fuel_config = self.controller.fuel_config
        self.expense_types = list(self.expenses_config.keys())
        self.validating_decimal = False
        self.validating_currency = False

        self.title("Configurações")
        if current_tab == 'expenses':
            self.geometry("400x400")
        elif current_tab == 'fuel':
            self.geometry('400x150')
        self.transient(master)
        self.grab_set()

        self.populate_config(current_tab)

        self.protocol('WM_DELETE_WINDOW', self.close)

    def populate_config(self, current_tab):
        if current_tab == 'expenses':
            self.create_expenses_config_frame()
            self.create_expenses_labels()
            self.create_min_wage_entry()
            self.create_percentages_entries('Capitais', 2)
            self.create_percentages_entries('Outras', 4)

        if current_tab == 'fuel':
            self.create_fuel_config_frame()
            self.create_fuel_cost_config_entry()
            self.create_avg_consumption_entry()

    def create_expenses_config_frame(self):
        self.expenses_config_frame = ttk.Frame(
            self,
            padding=10
        )
        self.expenses_config_frame.pack(padx=5, pady=2)
        self.refund_percentages_frame = ttk.LabelFrame(
            self.expenses_config_frame,
            text='Percentuais de Reembolso',
            padding=10
        )
        self.refund_percentages_frame.grid(
            row=1,
            column=0,
            columnspan=5,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_expenses_labels(self):
        for index, expense_type in enumerate(self.expense_types[1:], 1):
            self.refund_percentages_frame.grid_rowconfigure(
                index, weight=0
            )
            ttk.Label(
                self.refund_percentages_frame,
                text=expense_type,
                justify="right"
            ).grid(row=index+1, column=0, padx=5, pady=2)

        for col in range(6):
            self.expenses_config_frame.grid_columnconfigure(
                col, weight=0
            )
            self.expenses_config_frame.grid_columnconfigure(
                1, minsize=0
            )

        for index, location in enumerate(list(['Capitais', 'Outras'])):
            ttk.Label(
                self.refund_percentages_frame,
                text=location,
                justify='center',
            ).grid(row=1, column=(index+1)*2, padx=5, pady=2)

    def format_currency(self, float_value):
        formatted_value = f'R$ {float_value:,.2f}'
        return (
            formatted_value
            .replace(',', '#')
            .replace('.', ',')
            .replace('#', '.')
        )

    def validate_currency(
        self,
        value_var,
        config_dict,
        dict_key,
        *trace_info
    ):
        if self.validating_currency:
            return
        self.validating_currency = True

        try:
            value_str = value_var.get()
            value_raw = ''.join(filter(str.isdigit, value_str))

            if not value_raw:
                value_float = 0.0
            else:
                value_float = int(value_raw)/100

            value_var.set(self.format_currency(value_float))
            config_dict[dict_key] = value_float

        finally:
            self.validating_currency = False

    def create_min_wage_entry(self):
        min_wage_frame = ttk.LabelFrame(
            self.expenses_config_frame,
            text='Salário Mínimo'
        )
        min_wage_frame.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=5,
            pady=2,
            sticky='ew'
        )
        min_wage_var = Tk.StringVar(
            value=self.format_currency(
                self.expenses_config['Salário Mínimo']
            ))
        min_wage_var.trace_add(
            'write', self._validate_currency_callback(
                min_wage_var, self.expenses_config, 'Salário Mínimo'
                ))

        min_wage_entry = ttk.Entry(
            min_wage_frame,
            textvariable=min_wage_var,
            validate='all',
            validatecommand=(
                self.register(self.validate_entries_append),
                '%d',
                '%P',
                '%i',
                '%S'
            ),
            justify='right'
        )

        min_wage_entry.pack(fill=Tk.X, expand=True, padx=5, pady=2)
        min_wage_entry.bind("<Button-1>", self.push_caret_end)
        min_wage_entry.bind("<Key>", self.push_caret_end)

    def format_decimal(self, float_value):
        return f'{float_value:.1f}'.replace('.', ',')

    def validar_decimal(
        self,
        value_var,
        config_dict,
        dict_key,
        expense_location=None,
        *t
    ):
        if self.validating_decimal:
            return

        self.validating_decimal = True
        value_str = value_var.get()
        value_raw = ''.join(filter(str.isdigit, value_str))

        if not value_raw:
            value_float = 0.0
        else:
            value_float = int(value_raw)/10
        if value_float > 100.0:
            value_float = 100.0

        if config_dict == self.expenses_config:
            config_dict[dict_key][expense_location] = value_float
            value_var.set(self.format_decimal(value_float))

            percentage_capitals = config_dict[dict_key].get('Capitais', 0.0)
            percentage_others = config_dict[dict_key].get('Outras', 0.0)
            if percentage_capitals == percentage_others:
                self.expenses_config[dict_key][
                    'Irrelevante'
                ] = percentage_capitals
            else:
                self.expenses_config[dict_key]['Irrelevante'] = 0.0
        elif config_dict == self.fuel_config:
            config_dict[dict_key] = value_float
            value_var.set(self.format_decimal(value_float))

        self.validating_decimal = False

    def create_percentages_entries(self, location, column):
        for index, type in enumerate(self.expense_types[1:]):
            percentage_var = Tk.StringVar(
                value=self.format_decimal(
                    self.expenses_config[type][location]
                ))

            percentage_var.trace_add(
                'write',
                lambda *args,
                p=percentage_var,
                d=self.expenses_config,
                t=type,
                c=location: self.validar_decimal(
                    p, d, t, c, *args
                ))

            percentage_frame = ttk.Frame(self.refund_percentages_frame)
            percentage_frame.grid(
                row=index+2,
                column=column,
                padx=5,
                pady=2,
                sticky='ew'
            )

            percentage_entry = ttk.Entry(
                percentage_frame,
                textvariable=percentage_var,
                width=5,
                justify='right',
                validate='all',
                validatecommand=(
                    self.register(self.validate_entries_append),
                    '%d',
                    '%P',
                    '%i',
                    '%S'
                ))

            percentage_entry.pack(side=Tk.LEFT, padx=(0, 2))
            percentage_entry.bind("<Button-1>", self.push_caret_end)
            percentage_entry.bind("<Key>", self.push_caret_end)

            ttk.Label(
                percentage_frame,
                text='%',
                justify='left'
            ).pack(side=Tk.LEFT)

    def validate_entries_append(
        self,
        action_type,
        value_after,
        index,
        substring
    ):
        if action_type != '1':
            return True

        if int(index) >= len(value_after) - len(substring):
            return True

        return False

    def push_caret_end(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def close(self):
        self.main_window.update_tabs()
        self.destroy()

    def create_fuel_config_frame(self):
        self.fuel_config_frame = ttk.Frame(
            self,
            padding=10
        )
        self.fuel_config_frame.pack(fill=Tk.X, expand=True, anchor='center')

    def create_fuel_cost_config_entry(self):
        cost_var = Tk.StringVar(
            value=self.format_currency(self.fuel_config['custo_gas'])
        )
        cost_var.trace_add(
            'write', self._validate_currency_callback(
                cost_var, self.fuel_config, 'custo_gas'
            ))

        entry_frame = ttk.LabelFrame(
            self.fuel_config_frame,
            text='Preço do combustível por litro',
        )
        entry_frame.pack(
            side=Tk.TOP, fill=Tk.BOTH, expand=True, padx=5, pady=2
        )
        cost_entry = ttk.Entry(
            entry_frame,
            textvariable=cost_var,
            validate='all',
            validatecommand=(
                self.register(self.validate_entries_append),
                '%d',
                '%P',
                '%i',
                '%S'
            ), justify='right')
        cost_entry.pack(fill=Tk.X, expand=True, padx=5, pady=2)
        cost_entry.bind("<Button-1>", self.push_caret_end)
        cost_entry.bind("<Key>", self.push_caret_end)

    def create_avg_consumption_entry(self):
        avg_consumption_var = Tk.StringVar(
            value=self.format_decimal(self.fuel_config['consumo'])
        )
        avg_consumption_var.trace_add(
            'write', (
                lambda *args,
                v=avg_consumption_var,
                d=self.fuel_config,
                k='custo_gas',
                loc=None:
                    self.validar_decimal(v, d, k, loc, *args)
            ))

        entry_frame = ttk.LabelFrame(
            self.fuel_config_frame,
            text='Rendimento do veículo (km/L)',
        )
        entry_frame.pack(
            side=Tk.TOP, fill=Tk.BOTH, expand=True, padx=5, pady=2
        )
        config_entry = ttk.Entry(
            entry_frame,
            textvariable=avg_consumption_var,
            validate='all',
            validatecommand=(
                self.register(self.validate_entries_append),
                '%d',
                '%P',
                '%i',
                '%S'
            ), justify='right')
        config_entry.pack(fill=Tk.X, expand=True, padx=5, pady=2)
        config_entry.bind("<Button-1>", self.push_caret_end)
        config_entry.bind("<Key>", self.push_caret_end)

    def _validate_currency_callback(self, valor, config_dict, dict_key):
        return lambda *args: self.validate_currency(
            valor, config_dict, dict_key, *args
        )
