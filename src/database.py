import sqlite3 as sql
import pathlib
import os


class Database:
    def __init__(self):
        home_dir = pathlib.Path.home()

        if os.name == 'nt':
            db_path = os.getenv('LOCALAPPDATA')
            db_dir = pathlib.Path(db_path) / 'CalcViagens'
        else:
            db_dir = home_dir / 'DatabaseCalcViagens'

        db_dir.mkdir(parents=True, exist_ok=True)
        db_file = db_dir / 'viagens.db'
        self.conn = sql.connect(db_file)
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        create_trips_table_sql = '''CREATE TABLE IF NOT EXISTS trips (
            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_name TEXT NOT NULL
        );'''
        create_expenses_table_sql = '''CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT,
            expense_type TEXT NOT NULL,
            expense_location TEXT NOT NULL,
            expense_value REAL NOT NULL,
            trip_id INTEGER,
            FOREIGN KEY (trip_id)
            REFERENCES trips (trip_id) ON DELETE CASCADE
        );'''
        create_fuel_table_sql = ''' CREATE TABLE IF NOT EXISTS fuel(
            fuel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuel_date TEXT,
            fuel_route_start TEXT,
            fuel_route_end TEXT,
            fuel_distance TEXT NOT NULL,
            fuel_value REAL NOT NULL,
            trip_id INTEGER,
            FOREIGN KEY (trip_id)
            REFERENCES trips (trip_id) ON DELETE CASCADE
        );'''
        create_plane_tickets_table_sql = '''
        CREATE TABLE IF NOT EXISTS plane_tickets(
            plane_ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plane_ticket_start_date TEXT,
            plane_ticket_end_date TEXT,
            plane_ticket_route_start TEXT,
            plane_ticket_route_end TEXT,
            plane_ticket_value REAL NOT NULL,
            trip_id INTEGER,
            FOREIGN KEY (trip_id)
            REFERENCES trips (trip_id) ON DELETE CASCADE
        );'''

        self.cursor.execute(create_trips_table_sql)
        self.cursor.execute(create_expenses_table_sql)
        self.cursor.execute(create_fuel_table_sql)
        self.cursor.execute(create_plane_tickets_table_sql)
        self.conn.commit()

    def insert_trip(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        if trip_id:
            return trip_id
        else:
            insert_trip_sql = '''
                INSERT INTO trips (trip_name)
                VALUES (?);
            '''
            self.cursor.execute(insert_trip_sql, (trip_name_str,))
            self.conn.commit()
            trip_id = self.cursor.lastrowid
            return trip_id

    def add_expenses_data(self, expenses_data, trip_id):
        insert_expenses_data_sql = '''INSERT INTO expenses (
        expense_date, expense_type, expense_location, expense_value, trip_id
        ) VALUES (?, ?, ?, ?, ?)
        '''

        for expense in expenses_data:
            expense_date = expense['expense_date']
            expense_type = expense['expense_type']
            expense_location = expense['expense_location']
            expense_value = expense['expense_value']
            self.cursor.execute(
                insert_expenses_data_sql, (
                    expense_date,
                    expense_type,
                    expense_location,
                    expense_value,
                    trip_id
                ))

        self.conn.commit()

    def add_fuel_data(self, fuel_data, trip_id):
        insert_fuel_data_sql = '''INSERT INTO fuel (
            fuel_date,
            fuel_route_start,
            fuel_route_end,
            fuel_distance,
            fuel_value,
            trip_id
        ) VALUES (?, ?, ?, ?, ?, ?)
        '''

        for fuel in fuel_data:
            fuel_date = fuel['date_str']
            fuel_route_start = fuel['route_start_str']
            fuel_route_end = fuel['route_end_str']
            fuel_distance = fuel['distance_str']
            fuel_value = fuel['value_float']
            self.cursor.execute(
                insert_fuel_data_sql, (
                    fuel_date,
                    fuel_route_start,
                    fuel_route_end,
                    fuel_distance,
                    fuel_value,
                    trip_id
                ))

        self.conn.commit()

    def add_plane_tickets_data(self, plane_tickets_data, trip_id):
        insert_plane_tickets_data_sql = ''' INSERT INTO plane_tickets(
        plane_ticket_start_date,
        plane_ticket_end_date,
        plane_ticket_route_start,
        plane_ticket_route_end,
        plane_ticket_value,
        trip_id
        ) VALUES (?, ?, ?, ?, ?, ?)'''

        for plane_ticket in plane_tickets_data:
            plane_ticket_start_date = plane_ticket['start_date_str']
            plane_ticket_end_date = plane_ticket['end_date_str']
            plane_ticket_route_start = plane_ticket['route_start_str']
            plane_ticket_route_end = plane_ticket['route_end_str']
            plane_ticket_value = plane_ticket['value_float']
            self.cursor.execute(
                insert_plane_tickets_data_sql, (
                    plane_ticket_start_date,
                    plane_ticket_end_date,
                    plane_ticket_route_start,
                    plane_ticket_route_end,
                    plane_ticket_value,
                    trip_id
                )
            )

        self.conn.commit()

    def get_id(self, trip_name_str):
        get_trip_id_sql = '''
            SELECT trip_id FROM trips WHERE trip_name = ?;
        '''
        self.cursor.execute(get_trip_id_sql, (trip_name_str,))
        query_results = self.cursor.fetchone()

        if query_results:
            return query_results[0]
        else:
            return None

    def get_trip_names(self):
        get_trip_name_sql = '''
            SELECT trip_name from trips
        '''
        self.cursor.execute(get_trip_name_sql)
        query_results = self.cursor.fetchall()

        name = [name[0] for name in query_results]
        return name

    def del_trip_data(self, trip_id):
        del_expenses_sql = '''
            DELETE FROM expenses WHERE trip_id = ?;
        '''
        del_fuel_sql = '''
            DELETE FROM fuel WHERE trip_id = ?;
        '''

        del_plane_tickets_sql = '''
            DELETE FROM plane_tickets WHERE trip_id = ?;
        '''

        self.cursor.execute(del_expenses_sql, (trip_id,))
        self.cursor.execute(del_fuel_sql, (trip_id,))
        self.cursor.execute(del_plane_tickets_sql, (trip_id,))
        self.conn.commit()

    def get_db_expenses(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        get_expenses_data_sql = '''
            SELECT expense_date, expense_type, expense_location, expense_value
            FROM expenses
            WHERE trip_id = ?;
        '''
        self.cursor.execute(get_expenses_data_sql, (trip_id,))
        query_results = self.cursor.fetchall()

        expenses_rows = []
        for result in query_results:
            expense_row = {
                'date_str': result[0],
                'type_str': result[1],
                'location_str': result[2],
                'valor': result[3]
            }
            expenses_rows.append(expense_row)

        return expenses_rows

    def get_db_fuel(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        get_fuel_data_sql = '''
            SELECT
                fuel_date,
                fuel_route_start,
                fuel_route_end,
                fuel_distance,
                fuel_value
            FROM fuel
            WHERE trip_id = ?;
        '''
        self.cursor.execute(get_fuel_data_sql, (trip_id,))
        query_results = self.cursor.fetchall()

        fuel_rows = []
        for result in query_results:
            fuel_row = {
                'date_str': result[0],
                'route_start_str': result[1],
                'route_end_str': result[2],
                'distance_str': result[3],
                'valor': result[4]
            }
            fuel_rows.append(fuel_row)

        return fuel_rows

    def get_db_plane_tickets(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        get_plane_tickets_data_sql = '''
            SELECT
                plane_ticket_start_date,
                plane_ticket_end_date,
                plane_ticket_route_start,
                plane_ticket_route_end,
                plane_ticket_value
            FROM plane_tickets
            WHERE trip_id = ?;
        '''
        self.cursor.execute(get_plane_tickets_data_sql, (trip_id,))
        query_results = self.cursor.fetchall()

        plane_tickets_rows = []
        for result in query_results:
            plane_ticket_row = {
                'start_date_str': result[0],
                'end_date_str': result[1],
                'route_start_str': result[2],
                'route_end_str': result[3],
                'value_str': result[4]
            }
            plane_tickets_rows.append(plane_ticket_row)

        return plane_tickets_rows

    def del_trip(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        if trip_id:
            del_trip_sql = '''
                DELETE FROM trips
                WHERE trip_id = ?;
            '''

            self.cursor.execute(del_trip_sql, (trip_id,))
            self.conn.commit()
