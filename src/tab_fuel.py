import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class FuelTab:
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
        headers = {
            "Data": 10,
            "Trajeto": 30,
            "Distância": 15,
            "Valor": 10,
            "": 10
        }
        col_num = len(headers)
        for col in range(5):
            self.fuel_frame.grid_columnconfigure(
                col * 2,
                weight=0
            )
        for col, (header, width) in enumerate(headers.items()):
            ttk.Label(
                self.fuel_frame,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
                width=width
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_num - 1:
                ttk.Separator(
                    self.fuel_frame,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

    def create_row(self, db_fuel_data=None):
        if db_fuel_data:
            date_str = db_fuel_data['date_str']
            route_start_str = db_fuel_data['route_start_str']
            route_end_str = db_fuel_data['route_end_str']
            distance_str = db_fuel_data['distance_str']
        else:
            date_str = None
            route_start_str = None
            route_end_str = None
            distance_str = None

        fuel_row = {
            'date_str': date_str,
            'route_start_str': route_start_str,
            'route_end_str': route_end_str,
            'distance_str': distance_str
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
        if fuel_row['date_str']:
            date_datetime = datetime.strptime(
                fuel_row['date_str'], '%d/%m/%Y'
            )
            date_entry = ttk.DateEntry(
                self.fuel_frame,
                dateformat="%d/%m/%Y",
                width=10,
                startdate=date_datetime
            )

        else:
            date_entry = ttk.DateEntry(
                self.fuel_frame,
                dateformat="%d/%m/%Y",
                width=10,
                startdate=datetime.now()
            )
        fuel_row["date_var"] = date_entry
        date_entry.grid(
            row=row_num,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

    def create_route_field(self, fuel_row, row_num):
        route_frame = ttk.Frame(
            self.fuel_frame
        )
        route_frame.grid(row=row_num, column=2)
        if not fuel_row['route_start_str']:
            route_start_var = Tk.StringVar()
        else:
            route_start_var = Tk.StringVar(
                value=fuel_row['route_start_str']
            )
        if not fuel_row['route_end_str']:
            route_end_var = Tk.StringVar()
        else:
            route_end_var = Tk.StringVar(
                value=fuel_row['route_end_str']
            )
        for index, label in enumerate(['Origem', 'Destino']):
            fuel_row[f'route_label{index}'] = ttk.Label(
                route_frame,
                text=label,
                width=10
            )
            fuel_row[f'route_label{index}'].grid(
                row=index,
                column=0,
                padx=5,
                pady=2,
                sticky='w'
            )
        route_start = ttk.Entry(
            route_frame,
            textvariable=route_start_var,
            width=20
        )
        route_start.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )
        route_end = ttk.Entry(
            route_frame,
            textvariable=route_end_var,
            width=20
        )
        route_end.grid(
            row=1,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )

        fuel_row['route_frame'] = route_frame
        fuel_row['route_start_var'] = route_start_var
        fuel_row['route_end_var'] = route_end_var
        fuel_row['route_start_entry'] = route_start
        fuel_row['route_end_entry'] = route_end

    def create_distance_field(self, fuel_row, row_num):
        if not fuel_row['distance_str']:
            distance_var = Tk.StringVar()
        else:
            distance_var = Tk.StringVar(value=fuel_row['distance_str'])
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
            textvariable=distance_var,
            justify='right',
            width=15
        )
        km_label = ttk.Label(
            distance_frame,
            text='km'
        )

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

        fuel_row['km_label'] = km_label
        fuel_row['dist_entry'] = distance_entry
        fuel_row['distance_var'] = distance_var

        distance_var.trace_add(
            'write',
            lambda *args, r=fuel_row: self.validate_distance(r, *args)
        )

        fuel_row['dist_entry'].bind('<Key>', self.push_caret_end)
        fuel_row['dist_entry'].bind('<Button-1>', self.push_caret_end)

    def create_value_field(self, fuel_row, row_num):
        value_var = Tk.StringVar(value='R$ 0,00')
        fuel_row['value_var'] = value_var
        value_label = ttk.Label(
            self.fuel_frame,
            textvariable=value_var,
            anchor='e',
            width=5
        )
        value_label.grid(
            row=row_num,
            column=6,
            padx=5,
            pady=2,
            sticky='ew'
        )
        fuel_row['valor_entry'] = value_label

    def create_remover(self, fuel_row, row_num):
        fuel_row['remover'] = ttk.Button(
            self.fuel_frame,
            text='X',
            width=3,
            command=lambda: self.remove_row(fuel_row)
        )
        fuel_row['remover'].grid(row=row_num, column=8, padx=10, pady=2)

    def remove_row(self, fuel_row):
        for item in list(fuel_row.values()):
            if isinstance(item, Tk.Widget):
                item.destroy()
        self.fuel_rows.remove(fuel_row)

        self.regrid_widgets()

    def update_value(self, fuel_row):
        try:
            distance_str = fuel_row['distance_var'].get()
            distance_float = float(distance_str.replace(',', '.'))
        except (ValueError, AttributeError):
            distance_float = 0.0
        avg_consumption = self.config.get('consumo', 0.0)
        fuel_cost = self.config.get('custo_gas', 0.0)
        value = (fuel_cost * distance_float) / (avg_consumption)
        fuel_row['value_var'].set(f'R$ {value:.2f}'.replace('.', ','))

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

        value_str = fuel_row['distance_var'].get()
        value_raw = "".join(filter(str.isdigit, value_str))
        if not value_raw:
            value_float = 0.0
        else:
            value_float = int(value_raw) / 10

        fuel_row['distance_var'].set(self.format_distance(value_float))
        self.update_value(fuel_row)

        self.validating_distance = False

    def push_caret_end(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def get_fuel_data(self):
        fuel_data = []
        for fuel_row in self.fuel_rows:
            date_str = fuel_row['date_var'].entry.get()
            route_start_str = fuel_row['route_start_var'].get()
            route_end_str = fuel_row['route_end_var'].get()
            distance_str = fuel_row['distance_var'].get()
            value_raw = fuel_row['value_var'].get()
            value_str = (
                value_raw
                .replace('R$ ', '')
                .replace('.', '')
                .replace(',', '.')
            )
            value_float = float(value_str)

            fuel_entry = {
                'date_str': date_str,
                'route_start_str': route_start_str,
                'route_end_str': route_end_str,
                'distance_str': distance_str,
                'value_float': value_float
            }
            fuel_data.append(fuel_entry)
        return fuel_data

    def remove_fuel_rows(self, window_acton=None):
        for fuel_row in list(self.fuel_rows):
            self.remove_row(fuel_row)
        if not window_acton:
            self.create_row()

    def regrid_widgets(self):
        for index, fuel_row in enumerate(self.fuel_rows):
            row_num = index + 1
            fuel_row['date_var'].grid(
                row=row_num,
                column=0,
                padx=5,
                pady=2,
                sticky="ew"
            )
            fuel_row['route_frame'].grid(row=row_num, column=2)
            fuel_row['frame_dist'].grid(
                row=row_num,
                column=4,
            )
            fuel_row['valor_entry'].grid(
                row=row_num,
                column=6,
                padx=5,
                pady=2,
                sticky='ew'
            )
            fuel_row['remover'].grid(row=row_num, column=8, padx=10, pady=2)
