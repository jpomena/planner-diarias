import tkinter as Tk
import ttkbootstrap as ttk
from datetime import datetime


class PlaneTicketsTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.validating_currency = False

        self.plane_tickets_rows = []

    def create_tab_frame(self):
        canvas = ttk.Canvas(self.parent_frame)
        scrollbar = ttk.Scrollbar(
            self.parent_frame, orient="vertical", command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side='left', fill='both', expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.plane_tickets_frame = ttk.Frame(canvas)
        frame_id = canvas.create_window(
            (0, 0), window=self.plane_tickets_frame, anchor="nw"
        )

        def center_frame(event):
            canvas_width = event.width
            frame_width = self.plane_tickets_frame.winfo_reqwidth()
            x_pos = (canvas_width - frame_width) // 2
            canvas.coords(frame_id, x_pos if x_pos > 0 else 0, 0)

        def resize_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.plane_tickets_frame.bind("<Configure>", resize_frame)
        canvas.bind("<Configure>", center_frame)

    def create_headers(self):
        headers = {"Data": 10, "Trajeto": 35, "Valor": 20, "": 10}
        col_num = len(headers)
        for col in range(4):
            self.plane_tickets_frame.grid_columnconfigure(
                col * 2,
                weight=0
            )
        self.plane_tickets_frame.grid_columnconfigure(0, weight=0)
        for col, (header, width) in enumerate(headers.items()):
            ttk.Label(
                self.plane_tickets_frame,
                text=header,
                anchor="center",
                font=("Helvetica", 10, "bold"),
                width=width
            ).grid(row=0, column=col * 2, padx=5, pady=2, sticky="ew")
            if col < col_num - 1:
                ttk.Separator(
                    self.plane_tickets_frame,
                    orient="vertical",
                ).grid(row=0, column=col * 2 + 1, sticky="ns")

    def create_row(self, db_plane_tickets_data=None):
        if db_plane_tickets_data:
            start_date_str = db_plane_tickets_data['start_date_str']
            end_date_str = db_plane_tickets_data['end_date_str']
            route_start_str = db_plane_tickets_data['route_start_str']
            route_end_str = db_plane_tickets_data['route_end_str']
            value_str = db_plane_tickets_data['value_str']
        else:
            start_date_str = None
            end_date_str = None
            route_start_str = None
            route_end_str = None
            value_str = None

        plane_ticket_row = {
            'start_date_str': start_date_str,
            'end_date_str': end_date_str,
            'route_start_str': route_start_str,
            'route_end_str': route_end_str,
            'value_str': value_str
        }
        row_num = len(self.plane_tickets_rows) + 1

        self.create_date_field(plane_ticket_row, row_num)
        self.create_route_field(plane_ticket_row, row_num)
        self.create_value_field(plane_ticket_row, row_num)
        self.create_remover(plane_ticket_row, row_num)

        self.plane_tickets_rows.append(plane_ticket_row)

    def create_date_field(self, plane_ticket_row, row_num):
        date_frame = ttk.Frame(self.plane_tickets_frame)
        date_frame.grid(row=row_num, column=0)

        if plane_ticket_row['start_date_str']:
            start_date_datetime = datetime.strptime(
                plane_ticket_row['start_date_str'], '%d/%m/%Y'
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
        plane_ticket_row["start_date_var"] = start_date_entry
        start_date_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

        if plane_ticket_row['end_date_str']:
            end_date_datetime = datetime.strptime(
                plane_ticket_row['end_date_str'], '%d/%m/%Y'
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
        plane_ticket_row["end_date_var"] = end_date_entry
        end_date_entry.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky="ew"
        )

        plane_ticket_row['date_frame'] = date_frame

    def create_route_field(self, plane_ticket_row, row_num):
        route_frame = ttk.Frame(
            self.plane_tickets_frame
        )
        route_frame.grid(row=row_num, column=2)

        if not plane_ticket_row['route_start_str']:
            route_start_var = Tk.StringVar()
        else:
            route_start_var = Tk.StringVar(
                value=plane_ticket_row['route_start_str']
            )

        if not plane_ticket_row['route_end_str']:
            route_end_var = Tk.StringVar()
        else:
            route_end_var = Tk.StringVar(
                value=plane_ticket_row['route_end_str']
            )

        for index, label in enumerate(['Origem', 'Destino']):
            plane_ticket_row[f'route_label_{index}'] = ttk.Label(
                route_frame,
                text=label,
                width=10
            )
            plane_ticket_row[f'route_label_{index}'].grid(
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

        plane_ticket_row['route_frame'] = route_frame
        plane_ticket_row['route_start_var'] = route_start_var
        plane_ticket_row['route_end_var'] = route_end_var
        plane_ticket_row['route_start_entry'] = route_start
        plane_ticket_row['route_end_entry'] = route_end

    def create_value_field(self, plane_ticket_row, row_num):
        if not plane_ticket_row['value_str']:
            value_var = Tk.StringVar(value='R$ 0,00')
        else:
            value_var = Tk.StringVar(
                value=self.format_currency(plane_ticket_row['value_str']))
        value_var.trace_add(
            'write', self._validate_currency_callback(value_var))
        value_frame = ttk.Frame(
            self.plane_tickets_frame
        )
        plane_ticket_row['frame_value'] = value_frame
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

        plane_ticket_row['value_entry'] = value_entry
        plane_ticket_row['value_var'] = value_var
        plane_ticket_row['value_entry'].bind('<Key>', self.push_caret_end)
        plane_ticket_row['value_entry'].bind(
            '<Button-1>', self.push_caret_end
        )

    def create_remover(self, plane_ticket_row, row_num):
        plane_ticket_row['remover'] = ttk.Button(
            self.plane_tickets_frame,
            text='X',
            width=3,
            command=lambda: self.remove_row(plane_ticket_row)
        )
        plane_ticket_row['remover'].grid(
            row=row_num, column=6, padx=10, pady=2
        )

    def remove_row(self, plane_ticket_row):
        for item in list(plane_ticket_row.values()):
            if isinstance(item, Tk.Widget):
                item.destroy()
        self.plane_tickets_rows.remove(plane_ticket_row)

    def load_plane_tickets(self, db_plane_tickets_data):
        for entry in db_plane_tickets_data:
            self.create_row(entry)

    def push_caret_end(self, event):
        event.widget.after_idle(event.widget.icursor, 'end')

    def get_plane_tickets_data(self):
        plane_tickets_data = []
        for plane_ticket_row in self.plane_tickets_rows:
            start_date_str = plane_ticket_row['start_date_var'].entry.get()
            end_date_str = plane_ticket_row['end_date_var'].entry.get()
            route_start_str = plane_ticket_row['route_start_var'].get()
            route_end_str = plane_ticket_row['route_end_var'].get()
            value_raw = plane_ticket_row['value_var'].get()
            value_str = (
                value_raw
                .replace('R$ ', '')
                .replace('.', '')
                .replace(',', '.')
            )
            value_float = float(value_str)

            plane_tickets_entry = {
                'start_date_str': start_date_str,
                'end_date_str': end_date_str,
                'route_start_str': route_start_str,
                'route_end_str': route_end_str,
                'value_float': value_float
            }
            plane_tickets_data.append(plane_tickets_entry)
        return plane_tickets_data

    def remove_plane_tickets_rows(self, window_acton=None):
        for plane_ticket_row in list(self.plane_tickets_rows):
            self.remove_row(plane_ticket_row)
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
        for index, plane_ticket_row in enumerate(self.plane_tickets_rows):
            row_num = index + 1
            plane_ticket_row['date_frame'].grid(row=row_num, column=0)
            plane_ticket_row['route_frame'].grid(row=row_num, column=2)
            plane_ticket_row['frame_value'].grid(row=row_num, column=4)
            plane_ticket_row['remover'].grid(
                row=row_num, column=6, padx=10, pady=2
            )
