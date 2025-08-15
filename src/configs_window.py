import tkinter as Tk
import ttkbootstrap as ttk


class ConfigsWindow(Tk.Toplevel):
    def __init__(self, master, controller, configs):
        super().__init__(master)
        self.mw = master
        self.controller = controller
        self.configs = self.controller.configs
        self.tipos_config = list(self.configs.keys())
        self.validar_pct = False

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

        self.criar_labels()
        self.criar_entry_salario()
        self.criar_entry_porcentagens('Capitais', 2)
        self.criar_entry_porcentagens('Outras', 4)

        self.protocol('WM_DELETE_WINDOW', self.fechar)

    def criar_labels(self):
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

    def formatar_moeda(self, numero):
        formatted = f'R$ {numero:,.2f}'
        return formatted.replace(',', '#').replace('.', ',').replace('#', '.')

    def validar_moeda(self, *trace):
        sm_str = self.sm_var.get()
        sm_num = ''.join(filter(str.isdigit, sm_str))

        if not sm_num:
            sm_float = 0.0
        else:
            sm_float = int(sm_num)/100

        self.configs['Salário Mínimo'] = sm_float

        self.sm_var.trace_remove('write', self.trace_moeda)
        self.sm_var.set(self.formatar_moeda(sm_float))
        self.trace_moeda = self.sm_var.trace_add('write', self.validar_moeda)

    def criar_entry_salario(self):
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
            value=self.formatar_moeda(
                self.configs['Salário Mínimo']
            ))
        self.trace_moeda = self.sm_var.trace_add('write', self.validar_moeda)

        entry_sm = ttk.Entry(
            sm_frame,
            textvariable=self.sm_var,
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

    def formatar_porcentagens(self, numero):
        return f'{numero:.1f}'.replace('.', ',')

    def validar_porcentagens(self, pct_var, tipo_despesa, loc_despesa):
        if self.validar_pct:
            return

        self.validar_pct = True
        pct_str = pct_var.get()
        pct_num = ''.join(filter(str.isdigit, pct_str))

        if not pct_num:
            pct_float = 0.0
        else:
            pct_float = int(pct_num)/10
        if pct_float > 100.0:
            pct_float = 100.0

        self.configs[tipo_despesa][loc_despesa] = pct_float

        pct_var.set(self.formatar_porcentagens(pct_float))

        pct_cap = self.configs[tipo_despesa].get('Capitais', 0.0)
        pct_outras = self.configs[tipo_despesa].get('Outras', 0.0)
        if pct_cap == pct_outras:
            self.configs[tipo_despesa]['Irrelevante'] = pct_cap
        else:
            self.configs[tipo_despesa]['Irrelevante'] = 0.0

        self.validar_pct = False

    def criar_entry_porcentagens(self, loc, coluna):
        for index, tipo in enumerate(list(self.configs.keys())[1:]):
            pct_var = Tk.StringVar(
                value=self.formatar_porcentagens(
                    self.configs[tipo][loc]
                ))

            pct_var.trace_add(
                'write',
                lambda *args,
                v=pct_var,
                t=tipo,
                c=loc: self.validar_porcentagens(
                    v, t, c
                ))

            frame_entry = ttk.Frame(self.frame_pct)
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
