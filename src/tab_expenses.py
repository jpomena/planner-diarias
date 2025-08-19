import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class ExpensesTab:
    def __init__(self, parent_frame, controller):
        self.parent_frame = parent_frame
        self.controller = controller
        self.config = self.controller.expenses_config
        self.expense_types = self.controller.expense_types

        self.expenses_rows = []

    def create_tab_frame(self):
        canvas = ttk.Canvas(self.parent_frame)
        scrollbar = ttk.Scrollbar(
            self.parent_frame, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.expenses_frame = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.expenses_frame, anchor="nw"
        )

        def center_frame(event):
            canvas_width = event.width
            frame_width = self.expenses_frame.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def resize_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.expenses_frame.bind("<Configure>", resize_frame)
        canvas.bind("<Configure>", center_frame)

        def scroll_mouse(event):
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")

        for widget in [canvas, self.expenses_frame]:
            widget.bind("<MouseWheel>", scroll_mouse)
            widget.bind("<Button-4>", scroll_mouse)
            widget.bind("<Button-5>", scroll_mouse)

    def create_headers(self):
        headers = ["Data", "Tipo", "Localidade", "Valor", ""]
        col_num = len(headers)
        for col in range(5):
            self.expenses_frame.grid_columnconfigure(col * 2, weight=0)

        for col, header in enumerate(headers):
            ttk.Label(
                self.expenses_frame,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_num - 1:
                ttk.Separator(
                    self.expenses_frame,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

    def create_row(self, db_expenses_data=None):
        if db_expenses_data:
            date_str = db_expenses_data['date_str']
            type_str = db_expenses_data['type_str']
            location_str = db_expenses_data['location_str']
        else:
            date_str = None
            type_str = None
            location_str = None

        expense_row = {}
        row_num = len(self.expenses_rows) + 1
        self.create_date_field(
            expense_row, row_num, date_str
        )
        self.create_type_field(
            expense_row, row_num, type_str
        )
        self.create_location_field(expense_row, row_num, location_str)
        self.create_value_field(expense_row, row_num)
        self.update_location(expense_row, row_num)
        self.update_value(expense_row)
        self.create_remover(expense_row, row_num)

        self.expenses_rows.append(expense_row)

    def create_date_field(self, expense_row, row_num, date_str=None):
        if date_str:
            date_datetime = datetime.strptime(
                date_str, '%d/%m/%Y'
            )
            date_entry = ttk.DateEntry(
                self.expenses_frame,
                dateformat="%d/%m/%Y",
                startdate=date_datetime
            )

        else:
            date_entry = ttk.DateEntry(
                self.expenses_frame,
                dateformat="%d/%m/%Y",
                startdate=datetime.now()
            )
        expense_row['date_entry'] = date_entry
        expense_row['date_var'] = date_entry.entry
        date_entry.grid(
            row=row_num,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

    def create_type_field(self, expense_row, row_num, type_str=None):
        if type_str:
            type_var = Tk.StringVar(value=type_str)
        else:
            type_var = Tk.StringVar()
        expense_row['type_var'] = type_var

        expense_row['combobox_types'] = ttk.Combobox(
            self.expenses_frame,
            textvariable=type_var,
            values=self.expense_types,
            state="readonly",
        )
        expense_row["combobox_types"].grid(
            row=row_num,
            column=2,
            padx=5,
            pady=2,
            sticky="ew",
        )

        expense_row["combobox_types"].bind(
            "<<ComboboxSelected>>",
            lambda event, r=expense_row, r_n=row_num: (
                self.update_location(r, r_n),
                self.update_value(r),
            ))

    def create_location_field(self, expense_row, row_num, location_str=None):
        if location_str:
            location_var = Tk.StringVar(value=location_str)
        else:
            location_var = Tk.StringVar(value='Irrelevante')
        location_frame = ttk.Frame(self.expenses_frame)
        expense_row["relevant_location_frame"] = location_frame
        expense_row["irrelevant_location_frame"] = ttk.Label(
            self.expenses_frame,
            text="Irrelevante",
            anchor="center",
            width="20"
        )
        ttk.Radiobutton(
            location_frame,
            text="Capitais",
            value="Capitais",
            variable=location_var
        ).pack(side=Tk.LEFT, expand=True, fill=Tk.X, padx=5, pady=2)
        ttk.Radiobutton(
            location_frame,
            text="Outras",
            value="Outras",
            variable=location_var
        ).pack(side=Tk.LEFT, expand=True, fill=Tk.X, padx=5, pady=2)

        expense_row["location_var"] = location_var
        location_var.trace_add(
            "write",
            lambda *args,
            r=expense_row,
            r_n=row_num: self.update_value(
                r
            ))

    def location_relevant(self, expense_row, row_num):
        expense_row["irrelevant_location_frame"].grid_remove()
        expense_row["relevant_location_frame"].grid(
            row=row_num, column=4, padx=5, pady=2
        )

    def location_irrelevant(self, expense_row, row_num):
        expense_row["relevant_location_frame"].grid_remove()
        expense_row["irrelevant_location_frame"].grid(
            row=row_num, column=4, padx=5, pady=2
        )

    def create_value_field(self, expense_row, row_num):
        value_var = Tk.StringVar(value="R$ 0,00")
        expense_row["value_var"] = value_var

        expense_row["value_label"] = ttk.Label(
            self.expenses_frame,
            textvariable=expense_row["value_var"],
            anchor="e"
        )
        expense_row["value_label"].grid(
            row=row_num, column=6, padx=5, pady=2, sticky="ew"
        )

    def create_remover(self, expense_row, row_num):
        expense_row["remover"] = ttk.Button(
            self.expenses_frame,
            text="X",
            width=3,
            command=lambda: self.remove_row(expense_row),
        )
        expense_row["remover"].grid(row=row_num, column=8, padx=25, pady=2)

    def regrid_widgets(self, expenses_rows):
        for index, expense_row in enumerate(expenses_rows):
            row_num = index + 1
            expense_row['date_entry'].grid(
                row=row_num,
                column=0,
                padx=5,
                pady=2,
                sticky="ew"
            )
            expense_row['combobox_types'].grid(
                row=row_num,
                column=2,
                padx=5,
                pady=2,
                sticky="ew"
            )

            if expense_row['type_var'].get() in ["Almoço", "Janta"]:
                expense_row['irrelevant_location_frame'].grid_remove()
                expense_row['relevant_location_frame'].grid(
                    row=row_num,
                    column=4,
                    padx=5,
                    pady=2
                )
            else:
                expense_row['relevant_location_frame'].grid_remove()
                expense_row['irrelevant_location_frame'].grid(
                    row=row_num,
                    column=4,
                    padx=5,
                    pady=2
                )

            expense_row['value_label'].grid(
                row=row_num,
                column=6,
                padx=5,
                pady=2,
                sticky="ew"
            )
            expense_row['remover'].grid(
                row=row_num,
                column=8,
                padx=25,
                pady=2
            )

    def update_location(self, expense_row, row_num):
        type_str = expense_row["type_var"].get()
        if not type_str or type_str not in self.config:
            self.location_irrelevant(expense_row, row_num)
            return
        percentage_capitals = self.config[type_str]['Capitais']
        percentage_others = self.config[type_str]['Outras']

        if percentage_capitals != percentage_others:
            self.location_relevant(expense_row, row_num)
        else:
            self.location_irrelevant(expense_row, row_num)

    def update_value(self, expense_row):
        type_str = expense_row["type_var"].get()
        location_str = expense_row["location_var"].get()
        percentage = self.config.get(type_str, {}).get(location_str, 0.0)
        expense_row["value_var"].set(
            f'R$ {(self.config["Salário Mínimo"]/100)*percentage:.2f}'.replace(
                ".", ","
            ))

    def remove_row(self, expense_row):
        for widget in list(expense_row.values()):
            if isinstance(widget, Tk.Widget):
                widget.destroy()
        self.expenses_rows.remove(expense_row)

        # Flake8 Reclamaria que minha reclamação é longa e.e
        # noqa: E501 Porque cargas d'água o tkinter não tá esvaziando isso de imediato? Gambiarra:
        self.regrid_widgets(self.expenses_rows)

    def update_expenses_tab(self):
        for index, row in enumerate(self.expenses_rows):
            self.update_location(row, index+1)
            self.update_value(row)

    def load_expenses(self, db_expenses_data):
        for entry in db_expenses_data:
            self.create_row(entry)

    def remove_expenses_rows(self, window_action=None):
        for expense_row in list(self.expenses_rows):
            self.remove_row(expense_row)
        if not window_action:
            self.create_row()

    def get_expenses_data(self):
        expenses_data = []
        for expense_row in self.expenses_rows:
            date_str = expense_row['date_var'].get()
            type_str = expense_row['type_var'].get()
            location_str = expense_row['location_var'].get()
            value_str = expense_row['value_var'].get()
            value_float = float(
                value_str.replace('R$ ', '').replace('.', '').replace(',', '.')
            )
            percentage_capitals = self.config[type_str]['Capitais']
            percentage_others = self.config[type_str]['Outras']

            if percentage_capitals == percentage_others:
                location_str = 'Irrelevante'
            expense_entry = {
                'expense_date': date_str,
                'expense_type': type_str,
                'expense_location': location_str,
                'expense_value': value_float
            }
            expenses_data.append(expense_entry)
        return expenses_data
