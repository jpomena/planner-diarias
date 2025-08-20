import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class AccomodationsTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.validating_currency = False

        self.accomodations_rows = []

    def create_tab_frame(self):
        canvas = ttk.Canvas(self.parent_frame)
        scrollbar = ttk.Scrollbar(
            self.parent_frame, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.accomodations_frame = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.accomodations_frame, anchor="nw"
        )

        def center_frame(event):
            canvas_width = event.width
            frame_width = self.accomodations_frame.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def resize_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.accomodations_frame.bind("<Configure>", resize_frame)
        canvas.bind("<Configure>", center_frame)

    def create_headers(self):
        headers = {"Período": 10, "Local": 35, "Valor": 20, "": 10}
        col_num = len(headers)
        for col in range(4):
            self.accomodations_frame.grid_columnconfigure(
                col * 2,
                weight=0
            )
        self.accomodations_frame.grid_columnconfigure(0, weight=0)
        for col, (header, width) in enumerate(headers.items()):
            ttk.Label(
                self.accomodations_frame,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
                width=width
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_num - 1:
                ttk.Separator(
                    self.accomodations_frame,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

    def create_row(self, db_accomodations_data=None):
        if db_accomodations_data:
            start_date_str = db_accomodations_data['start_date_str']
            end_date_str = db_accomodations_data['end_date_str']
            location_str = db_accomodations_data['location_str']
            value_str = db_accomodations_data['value_str']
        else:
            start_date_str = None
            end_date_str = None
            location_str = None
            value_str = None

        accomodation_row = {
            'start_date_str': start_date_str,
            'end_date_str': end_date_str,
            'location_str': location_str,
            'value_str': value_str
        }
        row_num = len(self.accomodations_rows) + 1

        self.create_date_field(accomodation_row, row_num)
        self.create_route_field(accomodation_row, row_num)
        self.create_value_field(accomodation_row, row_num)
        self.create_remover(accomodation_row, row_num)

        self.accomodations_rows.append(accomodation_row)

    def create_date_field(self, accomodation_row, row_num):
        date_frame = ttk.Frame(self.accomodations_frame)
        date_frame.grid(row=row_num, column=0)

        if accomodation_row['start_date_str']:
            start_date_datetime = datetime.strptime(
                accomodation_row['start_date_str'], '%d/%m/%Y'
            )
            start_date_entry = ttk.DateEntry(
                date_frame,
                dateformat="%d/%m/%Y",
                width=10,
                startdate=start_date_datetime
            )
        else:
            start_date_entry = ttk.DateEntry(
                date_frame,
                dateformat="%d/%m/%Y",
                width=10,
                startdate=datetime.now()
            )
        accomodation_row["start_date_var"] = start_date_entry
        start_date_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

        if accomodation_row['end_date_str']:
            end_date_datetime = datetime.strptime(
                accomodation_row['end_date_str'], '%d/%m/%Y'
            )
            end_date_entry = ttk.DateEntry(
                date_frame,
                width=10,
                dateformat="%d/%m/%Y",
                startdate=end_date_datetime
            )

        else:
            end_date_entry = ttk.DateEntry(
                date_frame,
                width=10,
                dateformat="%d/%m/%Y",
                startdate=datetime.now()
            )
        accomodation_row["end_date_var"] = end_date_entry
        end_date_entry.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

        accomodation_row['date_frame'] = date_frame

    def create_route_field(self, accomodation_row, row_num):
        route_frame = ttk.Frame(
            self.accomodations_frame
        )
        route_frame.grid(row=row_num, column=2)

        if not accomodation_row['location_str']:
            location_var = Tk.StringVar()
        else:
            location_var = Tk.StringVar(
                value=accomodation_row['location_str']
            )

        location_entry = ttk.Entry(
            route_frame,
            textvariable=location_var,
            width=30
        )
        location_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )

        accomodation_row['route_frame'] = route_frame
        accomodation_row['location_var'] = location_var
        accomodation_row['location_entry'] = location_entry

    def create_value_field(self, accomodation_row, row_num):
        if not accomodation_row['value_str']:
            value_var = Tk.StringVar(value='R$ 0,00')
        else:
            value_var = Tk.StringVar(
                value=self.format_currency(accomodation_row['value_str']))
        value_var.trace_add(
            'write', self._validate_currency_callback(value_var))
        value_frame = ttk.Frame(
            self.accomodations_frame
        )
        accomodation_row['frame_value'] = value_frame
        value_frame.grid(
            row=row_num,
            column=4,
        )
        value_entry = ttk.Entry(
            value_frame,
            textvariable=value_var,
            width=15,
            validate='all',
            validatecommand=(
                (
                    self.parent_frame
                    .winfo_toplevel()
                    .register(self.validate_entries_append)),
                '%d',
                '%P',
                '%i',
                '%S'
            ), justify='right')
        value_entry.pack(
            side=Tk.LEFT,
            fill=Tk.BOTH,
            expand=True,
            padx=10,
            pady=2
        )

        accomodation_row['value_entry'] = value_entry
        accomodation_row['value_var'] = value_var
        accomodation_row['value_entry'].bind('<Key>', self.push_caret_end)
        accomodation_row['value_entry'].bind(
            '<Button-1>', self.push_caret_end
        )

    def create_remover(self, accomodation_row, row_num):
        accomodation_row['remover'] = ttk.Button(
            self.accomodations_frame,
            text='X',
            width=3,
            command=lambda: self.remove_row(accomodation_row)
        )
        accomodation_row['remover'].grid(
            row=row_num, column=6, padx=10, pady=2
        )

    def remove_row(self, accomodation_row):
        for item in list(accomodation_row.values()):
            if isinstance(item, Tk.Widget):
                item.destroy()
        self.accomodations_rows.remove(accomodation_row)

    def load_accomodations(self, db_accomodations_data):
        for entry in db_accomodations_data:
            self.create_row(entry)

    def push_caret_end(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def get_accomodations_data(self):
        accomodations_data = []
        for accomodation_row in self.accomodations_rows:
            start_date_str = accomodation_row['start_date_var'].entry.get()
            end_date_str = accomodation_row['end_date_var'].entry.get()
            location_str = accomodation_row['location_var'].get()
            value_raw = accomodation_row['value_var'].get()
            value_str = (
                value_raw
                .replace('R$ ', '')
                .replace('.', '')
                .replace(',', '.')
            )
            value_float = float(value_str)

            accomodations_entry = {
                'start_date_str': start_date_str,
                'end_date_str': end_date_str,
                'location_str': location_str,
                'value_float': value_float
            }
            accomodations_data.append(accomodations_entry)
        return accomodations_data

    def remove_accomodations_rows(self, window_acton=None):
        for accomodation_row in list(self.accomodations_rows):
            self.remove_row(accomodation_row)
        if not window_acton:
            self.create_row()

        self.regrid_widgets()

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

    def _validate_currency_callback(self, valor):
        return lambda *args: self.validate_currency(
            valor, *args
        )

    def validate_currency(
        self,
        value_var,
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

        finally:
            self.validating_currency = False

    def format_currency(self, float_value):
        formatted_value = f'R$ {float_value:,.2f}'
        return (
            formatted_value
            .replace(',', '#')
            .replace('.', ',')
            .replace('#', '.')
        )

    def regrid_widgets(self):
        for index, accomodation_row in enumerate(self.accomodations_rows):
            row_num = index + 1
            accomodation_row['date_frame'].grid(row=row_num, column=0)
            accomodation_row['route_frame'].grid(row=row_num, column=2)
            accomodation_row['frame_value'].grid(row=row_num, column=4)
            accomodation_row['remover'].grid(
                row=row_num, column=6, padx=10, pady=2
            )
