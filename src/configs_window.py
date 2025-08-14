import tkinter as Tk
import ttkbootstrap as ttk


class ConfigsWindow(Tk.Toplevel):
    def __init__(self, master, controller, configs):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.configs = configs
        self.tipos_config = list(self.configs.keys())

        self.title("Configurações")
        self.geometry("400x400")
        self.transient(master)
        self.grab_set()

        self.frame_configs = ttk.Frame(
            self,
            padding=10
        )
        self.frame_configs.pack(padx=5, pady=2)
        self.frame_pct = ttk.LabelFrame(
            self.frame_configs,
            text='Percentuais de Reembolso',
            padding=10
        )
        self.frame_pct.grid(
            row=1,
            column=0,
            columnspan=5,
            padx=5,
            pady=2,
            sticky='ew'
        )

        self.CriarLabels()
        self.CriarEntrySM()
        self.CriarEntrysCapitais()
        self.CriarEntrysOutras()

        self.protocol('WM_DELETE_WINDOW', self.Fechar)

    def CriarLabels(self):
        for index, config in enumerate(self.tipos_config[1:], 1):
            self.frame_pct.grid_rowconfigure(
                index, weight=0
            )
            ttk.Label(
                self.frame_pct,
                text=config,
                justify="right"
            ).grid(row=index+1, column=0, padx=5, pady=2)

        for col in range(6):
            self.frame_configs.grid_columnconfigure(
                col, weight=0
            )
            self.frame_configs.grid_columnconfigure(
                1, minsize=0
            )

        for index, tipo in enumerate(list(['Capitais', 'Outras'])):
            ttk.Label(
                self.frame_pct,
                text=tipo,
                justify='center',
            ).grid(row=1, column=(index+1)*2, padx=5, pady=2)

    def FormatarMoeda(self, numero):
        formatted = f'R$ {numero:,.2f}'
        return formatted.replace(',', '#').replace('.', ',').replace('#', '.')

    def ValidarMoeda(self, *trace):
        sm_str = self.sm_var.get()
        sm_num = ''.join(filter(str.isdigit, sm_str))

        if not sm_num:
            sm_float = 0.0
        else:
            sm_float = int(sm_num)/100

        self.configs['Salário Mínimo'] = sm_float

        self.sm_var.trace_remove('write', self.trace_moeda)
        self.sm_var.set(self.FormatarMoeda(sm_float))
        self.trace_moeda = self.sm_var.trace_add('write', self.ValidarMoeda)

    def CriarEntrySM(self):
        sm_frame = ttk.LabelFrame(
            self.frame_configs,
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
        self.sm_var = Tk.StringVar(
            value=self.FormatarMoeda(
                self.configs['Salário Mínimo']
            ))
        self.trace_moeda = self.sm_var.trace_add('write', self.ValidarMoeda)

        entry_sm = ttk.Entry(
            sm_frame,
            textvariable=self.sm_var,
            justify='right'
        )
        entry_sm.pack(fill=Tk.X, expand=True, padx=5, pady=2)

    def FormatarPct(self, numero):
        return f'{numero:.1f}'.replace('.', ',')

    def ValidarPctCapitais(self, tipo, pct_var, trace_pct_cap, *trace):
        pct_str = pct_var.get()
        pct_num = ''.join(filter(str.isdigit, pct_str))

        if not pct_num:
            pct_float = 0.0
        else:
            pct_float = int(pct_num)/10
        self.configs[tipo]['Capitais'] = pct_float

        pct_var.trace_remove('write', self.trace_pct_cap)
        pct_var.set(self.FormatarPct(pct_float))
        self.trace_pct_cap = pct_var.trace_add(
            'write', lambda *args, t=tipo, p=pct_var, tp=self.trace_pct_cap:
            self.ValidarPctCapitais(t, p, tp, *args)
        )

    def CriarEntrysCapitais(self):
        for index, tipo in enumerate(list(self.configs.keys())[1:]):
            pct_var = Tk.StringVar(
                value=self.FormatarPct(
                    self.configs[tipo]['Capitais']
                ))
            setattr(
                self,
                f'pct_var_{tipo}',
                pct_var
            )

            self.trace_pct_cap = pct_var.trace_add(
                'write', lambda *args, t=tipo, p=pct_var, trace_pct=None:
                self.ValidarPctCapitais(t, p, trace_pct, *args)
            )
            pct_var.trace_add(
                'write',
                lambda *args, t=tipo, p=pct_var, tp=self.trace_pct_cap:
                self.ValidarPctCapitais(t, p, tp, *args)
            )

            frame_entry = ttk.Frame(self.frame_pct)
            frame_entry.grid(
                row=index+2,
                column=2,
                padx=5,
                pady=2,
                sticky='ew'
            )

            ttk.Entry(
                frame_entry,
                textvariable=pct_var,
                width=5,
                justify='right'
            ).pack(side=Tk.LEFT, padx=(0, 2))

            ttk.Label(
                frame_entry,
                text='%',
                justify='left'
            ).pack(side=Tk.LEFT)

    def ValidarPctOutras(self, tipo, pct_var, trace_pct_out, *trace):
        pct_str = pct_var.get()
        pct_num = ''.join(filter(str.isdigit, pct_str))

        if not pct_num:
            pct_float = 0.0
        else:
            pct_float = int(pct_num)/10
        self.configs[tipo]['Outras'] = pct_float

        pct_var.trace_remove('write', self.trace_pct_out)
        pct_var.set(self.FormatarPct(pct_float))
        self.trace_pct_out = pct_var.trace_add(
            'write', lambda *args, t=tipo, p=pct_var, tp=self.trace_pct_out:
            self.ValidarPctOutras(t, p, tp, *args)
        )

    def CriarEntrysOutras(self):
        for index, tipo in enumerate(list(self.configs.keys())[1:]):
            pct_var = Tk.StringVar(
                value=self.FormatarPct(
                    self.configs[tipo]['Outras']
                ))
            setattr(
                self,
                f'pct_var_{tipo}',
                pct_var
            )

            self.trace_pct_out = pct_var.trace_add(
                'write', lambda *args, t=tipo, p=pct_var, trace_pct=None:
                self.ValidarPctOutras(t, p, trace_pct, *args)
            )
            pct_var.trace_add(
                'write',
                lambda *args, t=tipo, p=pct_var, tp=self.trace_pct_out:
                self.ValidarPctOutras(t, p, tp, *args)
            )

            frame_entry = ttk.Frame(self.frame_pct)
            frame_entry.grid(
                row=index+2,
                column=4,
                padx=5,
                pady=2,
                sticky='ew'
            )

            ttk.Entry(
                frame_entry,
                textvariable=pct_var,
                width=5,
                justify='right'
            ).pack(side=Tk.LEFT, padx=(0, 2))

            ttk.Label(
                frame_entry,
                text='%',
                justify='left'
            ).pack(side=Tk.LEFT)

    def Fechar(self):
        self.controller.AtualizarLinhas()
        self.destroy()
