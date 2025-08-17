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
        create_trips_table_sql = '''CREATE TABLE IF NOT EXISTS viagens (
            id_viagem INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_viagem TEXT NOT NULL
        );'''
        create_expenses_table_sql = '''CREATE TABLE IF NOT EXISTS despesas (
            id_despesa INTEGER PRIMARY KEY AUTOINCREMENT,
            data_despesa TEXT,
            tipo_despesa TEXT NOT NULL,
            loc_despesa TEXT NOT NULL,
            valor_despesa REAL NOT NULL,
            id_viagem INTEGER,
            FOREIGN KEY (id_viagem)
            REFERENCES viagens (id_viagem) ON DELETE CASCADE
        );'''
        create_fuel_table_sql = ''' CREATE TABLE IF NOT EXISTS gas(
            id_gas INTEGER PRIMARY KEY AUTOINCREMENT,
            data_gas TEXT,
            destino_gas TEXT,
            dist_gas TEXTO NOT NULL,
            valor_gas REAL NOT NULL,
            id_viagem INTEGER,
            FOREIGN KEY (id_viagem)
            REFERENCES viagens (id_viagem) ON DELETE CASCADE
        );'''
        self.cursor.execute(create_trips_table_sql)
        self.cursor.execute(create_expenses_table_sql)
        self.cursor.execute(create_fuel_table_sql)
        self.conn.commit()

    def insert_trip(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        if trip_id:
            return trip_id
        else:
            insert_trip_sql = '''
                INSERT INTO viagens (nome_viagem)
                VALUES (?);
            '''
            self.cursor.execute(insert_trip_sql, (trip_name_str,))
            self.conn.commit()
            trip_id = self.cursor.lastrowid
            return trip_id

    def add_trip_data(self, expenses_data, fuel_data, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        self.del_trip_data(trip_id)

        insert_expenses_data_sql = '''INSERT INTO despesas (
        data_despesa, tipo_despesa, loc_despesa, valor_despesa, id_viagem
        ) VALUES (?, ?, ?, ?, ?)
        '''
        inser_fuel_data_sql = '''INSERT INTO gas(
        data_gas, destino_gas, dist_gas, valor_gas, id_viagem
        ) VALUES (?, ?, ?, ?, ?)
        '''

        for expense in expenses_data:
            expense_date = expense['data_desp']
            expense_type = expense['tipo_desp']
            expense_location = expense['loc_desp']
            expense_value = expense['valor_desp']
            self.cursor.execute(
                insert_expenses_data_sql, (
                    expense_date,
                    expense_type,
                    expense_location,
                    expense_value,
                    trip_id
                ))

        for fuel in fuel_data:
            fuel_date = fuel['data_gas']
            fuel_route = fuel['destino_gas']
            fuel_distance = fuel['dist_gas']
            fuel_value = fuel['valor_gas']
            self.cursor.execute(
                inser_fuel_data_sql, (
                    fuel_date, fuel_route, fuel_distance, fuel_value, trip_id
                ))

        self.conn.commit()

    def get_id(self, trip_name_str):
        get_trip_id_sql = '''
            SELECT id_viagem FROM viagens WHERE nome_viagem = ?;
        '''
        self.cursor.execute(get_trip_id_sql, (trip_name_str,))
        query_results = self.cursor.fetchone()

        if query_results:
            return query_results[0]
        else:
            return None

    def get_trip_names(self):
        get_trip_name_sql = '''
            SELECT nome_viagem from viagens
        '''
        self.cursor.execute(get_trip_name_sql)
        query_results = self.cursor.fetchall()

        name = [name[0] for name in query_results]
        return name

    def del_trip_data(self, trip_id):
        del_expenses_sql = '''
            DELETE FROM despesas WHERE id_viagem = ?;
        '''
        del_fuel_sql = '''
            DELETE FROM gas WHERE id_viagem = ?;
        '''

        self.cursor.execute(del_expenses_sql, (trip_id,))
        self.cursor.execute(del_fuel_sql, (trip_id,))
        self.conn.commit()

    def get_db_expenses(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        get_expenses_data_sql = '''
            SELECT data_despesa, tipo_despesa, loc_despesa, valor_despesa
            FROM despesas
            WHERE id_viagem = ?;
        '''
        self.cursor.execute(get_expenses_data_sql, (trip_id,))
        query_results = self.cursor.fetchall()

        expenses_data = []
        for result in query_results:
            expense = {
                'data': result[0],
                'tipo': result[1],
                'loc': result[2],
                'valor': result[3]
            }
            expenses_data.append(expense)

        return expenses_data

    def get_db_fuel(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        get_fuel_data_sql = '''
            SELECT data_gas, destino_gas, dist_gas, valor_gas
            FROM gas
            WHERE id_viagem = ?;
        '''
        self.cursor.execute(get_fuel_data_sql, (trip_id,))
        query_results = self.cursor.fetchall()

        fuel_data = []
        for result in query_results:
            fuel = {
                'data': result[0],
                'destino': result[1],
                'dist': result[2],
                'valor': result[3]
            }
            fuel_data.append(fuel)
        return fuel_data

    def del_trip(self, trip_name_str):
        trip_id = self.get_id(trip_name_str)
        if trip_id:
            del_trip_sql = '''
                DELETE FROM viagens
                WHERE id_viagem = ?;
            '''

            self.cursor.execute(del_trip_sql, (trip_id,))
            self.conn.commit()
