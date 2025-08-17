import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class AbaGas:
    def __init__(self, parent_frame, controller):
        self.parent_frame = parent_frame
        self.controller = controller
        self.config = self.controller.fuel_config
        self.validating_distance = False

        self.fuel_rows = []

    def create_tab_frame(self):
        canvas = ttk.Canvas(self.parent_frame)
        scrollbar = ttk.Scrollbar(
            self.parent_frame, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.fuel_frame = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.fuel_frame, anchor="nw"
        )

        def center_frame(event):
            canvas_width = event.width
            frame_width = self.fuel_frame.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def resize_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.fuel_frame.bind("<Configure>", resize_frame)
        canvas.bind("<Configure>", center_frame)

    def create_headers(self):
        headers = ["Data", "Trajeto", "Distância", "Valor", ""]
        col_num = len(headers)
        for col in range(5):
            self.fuel_frame.grid_columnconfigure(col * 2, weight=0)

        for col, header in enumerate(headers):
            ttk.Label(
                self.fuel_frame,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_num - 1:
                ttk.Separator(
                    self.fuel_frame,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

    def create_row(self, db_fuel_data=None):
        if db_fuel_data:
            date_str = db_fuel_data['data']
            route_str = db_fuel_data['destino']
            distance_str = db_fuel_data['dist']
        else:
            date_str = None
            route_str = None
            distance_str = None

        fuel_row = {
            'data_gas': date_str,
            'destino_gas': route_str,
            'dist_gas': distance_str
        }
        row_num = len(self.fuel_rows) + 1

        self.create_date_field(fuel_row, row_num)
        self.create_route_field(fuel_row, row_num)
        self.create_distance_field(fuel_row, row_num)
        self.create_value_field(fuel_row, row_num)
        self.create_remover(fuel_row, row_num)
        self.update_value(fuel_row)

        self.fuel_rows.append(fuel_row)

    def create_date_field(self, fuel_row, row_num):
        if fuel_row['data_gas']:
            date_datetime = datetime.strptime(
                fuel_row['data_gas'], '%d/%m/%Y'
            )
            data_entry = ttk.DateEntry(
                self.fuel_frame,
                dateformat="%d/%m/%Y",
                startdate=date_datetime
            )

        else:
            data_entry = ttk.DateEntry(
                self.fuel_frame,
                dateformat="%d/%m/%Y",
                startdate=datetime.now()
            )
        fuel_row["data_entry"] = data_entry
        fuel_row["data_gas"] = data_entry.entry
        data_entry.grid(
            row=row_num,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

    def create_route_field(self, fuel_row, row_num):
        if not fuel_row['destino_gas']:
            fuel_row['destino_gas'] = Tk.StringVar()
        else:
            fuel_row['destino_gas'] = Tk.StringVar(
                value=fuel_row['destino_gas']
            )

        route_entry = ttk.Entry(
            self.fuel_frame,
            textvariable=fuel_row['destino_gas']
        )
        route_entry.grid(
            row=row_num,
            column=2,
            padx=5,
            pady=2,
            sticky='ew'
        )
        fuel_row['destino_entry'] = route_entry

    def create_distance_field(self, fuel_row, row_num):
        if not fuel_row['dist_gas']:
            fuel_row['dist_gas'] = Tk.StringVar()
        else:
            fuel_row['dist_gas'] = Tk.StringVar(value=fuel_row['dist_gas'])
        distance_frame = ttk.Frame(
            self.fuel_frame
        )
        fuel_row['frame_dist'] = distance_frame
        distance_frame.grid(
            row=row_num,
            column=4,
        )
        distance_entry = ttk.Entry(
            distance_frame,
            textvariable=fuel_row['dist_gas'],
            justify='right'
        )
        fuel_row['dist_entry'] = distance_entry
        km_label = ttk.Label(
            distance_frame,
            text='km'
        )
        fuel_row['km_label'] = km_label
        distance_entry.pack(
            side=Tk.LEFT,
            fill=Tk.BOTH,
            expand=True,
            padx=5,
            pady=2
        )
        km_label.pack(
            side=Tk.LEFT
        )
        fuel_row['dist_gas'].trace_add(
            'write',
            lambda *args, r=fuel_row: self.validate_distance(r, *args)
        )
        fuel_row['dist_entry'].bind('<Key>', self.push_caret_end)
        fuel_row['dist_entry'].bind('<Button-1>', self.push_caret_end)

    def create_value_field(self, fuel_row, row_num):
        value_var = Tk.StringVar(value='R$ 0,00')
        fuel_row['valor_gas'] = value_var
        value_label = ttk.Label(
            self.fuel_frame,
            textvariable=fuel_row['valor_gas'],
            justify='right'
        )
        value_label.grid(
            row=row_num,
            column=6,
            padx=5,
            pady=2
        )
        fuel_row['valor_entry'] = value_label

    def create_remover(self, fuel_row, row_num):
        fuel_row['removedor'] = ttk.Button(
            self.fuel_frame,
            text='X',
            width=3,
            command=lambda: self.remove_row(fuel_row)
        )
        fuel_row['removedor'].grid(row=row_num, column=8, padx=25, pady=2)

    def remove_row(self, fuel_row):
        for item in list(fuel_row.values()):
            if isinstance(item, Tk.Widget):
                item.destroy()
        self.fuel_rows.remove(fuel_row)

    def update_value(self, fuel_row):
        try:
            distance_str = fuel_row.get('dist_gas').get()
            distance_float = float(distance_str.replace(',', '.'))
        except ValueError:
            distance_float = 0.0
        avg_consumption = self.config.get('consumo', 0.0)
        fuel_cost = self.config.get('custo_gas', 0.0)
        value = (fuel_cost * distance_float) / (avg_consumption)
        fuel_row['valor_gas'].set(f'R$ {value:.2f}'.replace('.', ','))

    def update_fuel_tab(self):
        for fuel_row in self.fuel_rows:
            self.update_value(fuel_row)

    def load_fuel(self, db_fuel_data):
        for entry in db_fuel_data:
            self.create_row(entry)

    def format_distance(self, num_float,):
        return f'{num_float:.1f}'.replace('.', ',')

    def validate_distance(self, fuel_row, *args):
        if self.validating_distance:
            return
        self.validating_distance = True

        value_str = fuel_row['dist_gas'].get()
        value_raw = "".join(filter(str.isdigit, value_str))
        if not value_raw:
            value_float = 0.0
        else:
            value_float = int(value_raw) / 10

        fuel_row['dist_gas'].set(self.format_distance(value_float))
        self.update_value(fuel_row)

        self.validating_distance = False

    def push_caret_end(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def get_fuel_data(self):
        fuel_data = []
        for fuel_row in self.fuel_rows:
            data_str = fuel_row['data_gas'].get()
            try:
                tipo_str = fuel_row['destino_gas'].get()
            except AttributeError:
                tipo_str = fuel_row['destino_gas']
            location_str = fuel_row['dist_gas'].get()
            value_raw = fuel_row['valor_gas'].get()
            value_str = (
                value_raw
                .replace('R$ ', '')
                .replace('.', '')
                .replace(',', '.')
            )
            value_float = float(value_str)

            fuel_entry = {
                'data_gas': data_str,
                'destino_gas': tipo_str,
                'dist_gas': location_str,
                'valor_gas': value_float
            }
            fuel_data.append(fuel_entry)
        return fuel_data

    def remove_fuel_rows(self, window_acton=None):
        for fuel_row in list(self.fuel_rows):
            self.remove_row(fuel_row)
        if not window_acton:
            self.create_row()
