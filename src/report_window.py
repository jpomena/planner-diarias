import tkinter as Tk
import ttkbootstrap as ttk


class ReportWindow(Tk.Toplevel):
    def __init__(self, master, expenses_rows):
        super().__init__(master)
        self.master = master
        self.title('Resumo')
        self.geometry('600x600')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.expenses_rows = expenses_rows

        self.report_frame = ttk.Frame(
            self
        )
        self.report_frame.pack(fill=Tk.BOTH, expand=True, padx=5, pady=2)

        self.create_expenses_table()
        self.fill_expenses_table()
        self.create_totals_table()
        self.fill_totals_table()

    def create_expenses_table(self):
        columns_ids = ['date_str', 'type_str', 'location_str', 'val']
        headers = {
            'date_str': 'date_str',
            'type_str': 'Tipo de Despesa',
            'location_str': 'Localidade',
            'val': 'Valor'
        }

        table_frame = ttk.LabelFrame(
            self.report_frame,
            text='expenses',
            padding=10
        )
        table_frame.pack(side=Tk.TOP, fill=Tk.BOTH, padx=5, pady=5)

        self.expenses_table = ttk.Treeview(
            table_frame,
            columns=columns_ids,
            show='headings'
        )
        self.expenses_table.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

        for col in columns_ids:
            self.expenses_table.heading(f'{col}', text=f'{headers[col]}')
            self.expenses_table.column(col, width=75, anchor='center')

        expenses_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=Tk.VERTICAL,
            command=self.expenses_table.yview
        )
        expenses_scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.expenses_table.configure(yscrollcommand=expenses_scrollbar.set)

    def fill_expenses_table(self):
        for expense_row in self.expenses_rows:
            date_str = expense_row['date_var'].get()
            type_str = expense_row['type_var'].get()
            location_str = expense_row['location_var'].get()
            value_str = expense_row['value_var'].get()
            if type_str != 'Almoço' and type_str != 'Janta':
                location_str = 'Irrelevante'
            self.expenses_table.insert(
                '',
                'end',
                values=(
                    date_str,
                    type_str,
                    location_str,
                    value_str
                ))

    def create_totals_table(self):
        totals_frame = ttk.LabelFrame(
            self.report_frame,
            text='Totais',
            padding=10
        )
        totals_frame.pack(
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
        self.totals_table = ttk.Treeview(
            totals_frame,
            columns=columns_ids,
            show='headings'
        )
        self.totals_table.pack(
            fill=Tk.BOTH,
            expand=True,
            padx=5,
            pady=2
            )
        for col in columns_ids:
            self.totals_table.heading(f'{col}', text=f'{headers[col]}')
            self.totals_table.column(col, width=100, anchor='center')

    def fill_totals_table(self):
        expense_types = [
            'Lanche em Trajeto',
            'Café da Manhã',
            'Almoço',
            'Café da Tarde',
            'Janta',
            'Total'
        ]
        expenses_totals = {}

        for type in expense_types:
            expenses_totals[f'{type}'] = 0.0

        for expense_row in self.expenses_rows:
            type_str = expense_row['type_var'].get()
            value_str = expense_row['value_var'].get()
            value_float = float(value_str.replace('R$ ', '').replace(',', '.'))
            expenses_totals[f'{type_str}'] += value_float
            expenses_totals['Total'] += value_float

        for type in expense_types:
            self.totals_table.insert(
                '',
                'end',
                values=(
                    f'{type}', (f'R$ {expenses_totals[type]:.2f}').replace(
                        '.', ','
                    )))
