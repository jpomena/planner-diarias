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

        self.criar_tabelas()

    def criar_tabelas(self):
        gerar_tab_viagens = '''CREATE TABLE IF NOT EXISTS viagens (
            id_viagem INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_viagem TEXT NOT NULL
        );'''
        gerar_tab_despesas = '''CREATE TABLE IF NOT EXISTS despesas (
            id_despesa INTEGER PRIMARY KEY AUTOINCREMENT,
            data_despesa TEXT,
            tipo_despesa TEXT NOT NULL,
            loc_despesa TEXT NOT NULL,
            valor_despesa REAL NOT NULL,
            id_viagem INTEGER,
            FOREIGN KEY (id_viagem)
            REFERENCES viagens (id_viagem) ON DELETE CASCADE
        );'''
        gerar_tab_gas = ''' CREATE TABLE IF NOT EXISTS gas(
            id_gas INTEGER PRIMARY KEY AUTOINCREMENT,
            data_gas TEXT,
            destino_gas TEXT,
            dist_gas TEXTO NOT NULL,
            valor_gas REAL NOT NULL,
            id_viagem INTEGER,
            FOREIGN KEY (id_viagem)
            REFERENCES viagens (id_viagem) ON DELETE CASCADE
        );'''
        self.cursor.execute(gerar_tab_viagens)
        self.cursor.execute(gerar_tab_despesas)
        self.cursor.execute(gerar_tab_gas)
        self.conn.commit()

    def add_viagem(self, nome_viagem_str):
        id_viagem = self.get_id(nome_viagem_str)
        if id_viagem:
            return id_viagem
        else:
            sql_add_viagem = '''
                INSERT INTO viagens (nome_viagem)
                VALUES (?);
            '''
            self.cursor.execute(sql_add_viagem, (nome_viagem_str,))
            self.conn.commit()
            id_viagem = self.cursor.lastrowid
            return id_viagem

    def add_dados_viagem(self, dados_despesas, dados_gas, nome_viagem_str):
        id_viagem = self.get_id(nome_viagem_str)
        self.del_dados_viagem(id_viagem)

        sql_add_despesas = '''INSERT INTO despesas (
        data_despesa, tipo_despesa, loc_despesa, valor_despesa, id_viagem
        ) VALUES (?, ?, ?, ?, ?)
        '''
        sql_add_gas = '''INSERT INTO gas(
        data_gas, destino_gas, dist_gas, valor_gas, id_viagem
        ) VALUES (?, ?, ?, ?, ?)
        '''

        for entrada in dados_despesas:
            data_desp = entrada['data_desp']
            tipo_desp = entrada['tipo_desp']
            loc_desp = entrada['loc_desp']
            valor_desp = entrada['valor_desp']
            self.cursor.execute(
                sql_add_despesas, (
                    data_desp, tipo_desp, loc_desp, valor_desp, id_viagem
                ))

        for entrada in dados_gas:
            data_gas = entrada['data_gas']
            destino_gas = entrada['destino_gas']
            dist_gas = entrada['dist_gas']
            valor_gas = entrada['valor_gas']
            self.cursor.execute(
                sql_add_gas, (
                    data_gas, destino_gas, dist_gas, valor_gas, id_viagem
                ))

        self.conn.commit()

    def get_id(self, nome_viagem):
        sql_query_nome = '''
            SELECT id_viagem FROM viagens WHERE nome_viagem = ?;
        '''
        self.cursor.execute(sql_query_nome, (nome_viagem,))
        resultado = self.cursor.fetchone()

        if resultado:
            return resultado[0]
        else:
            return None

    def get_nome_viagens(self):
        sql_obter_nomes = '''
            SELECT nome_viagem from viagens
        '''
        self.cursor.execute(sql_obter_nomes)
        resultado_query = self.cursor.fetchall()

        nomes = [nome[0] for nome in resultado_query]
        return nomes

    def del_dados_viagem(self, id_viagem):
        sql_delete_despesas = '''
            DELETE FROM despesas WHERE id_viagem = ?;
        '''
        sql_delete_gas = '''
            DELETE FROM gas WHERE id_viagem = ?;
        '''

        self.cursor.execute(sql_delete_despesas, (id_viagem,))
        self.cursor.execute(sql_delete_gas, (id_viagem,))
        self.conn.commit()

    def get_despesas_db(self, nome_viagem):
        id_viagem = self.get_id(nome_viagem)
        sql_despesas_viagem = '''
            SELECT data_despesa, tipo_despesa, loc_despesa, valor_despesa
            FROM despesas
            WHERE id_viagem = ?;
        '''
        self.cursor.execute(sql_despesas_viagem, (id_viagem,))
        resultados = self.cursor.fetchall()

        despesas_viagem = []
        for resultado in resultados:
            dados_despesa = {
                'data': resultado[0],
                'tipo': resultado[1],
                'loc': resultado[2],
                'valor': resultado[3]
            }
            despesas_viagem.append(dados_despesa)

        return despesas_viagem

    def get_gas_db(self, nome_viagem):
        id_viagem = self.get_id(nome_viagem)
        sql_gas_viagem = '''
            SELECT data_gas, destino_gas, dist_gas, valor_gas
            FROM gas
            WHERE id_viagem = ?;
        '''
        self.cursor.execute(sql_gas_viagem, (id_viagem,))
        resultados = self.cursor.fetchall()

        gas_viagem = []
        for resultado in resultados:
            dados_gas = {
                'data': resultado[0],
                'destino': resultado[1],
                'dist': resultado[2],
                'valor': resultado[3]
            }
            gas_viagem.append(dados_gas)
        return gas_viagem

    def del_viagem(self, nome_viagem):
        id_viagem = self.get_id(nome_viagem)
        if id_viagem:
            sql_deletar_viagem = '''
                DELETE FROM viagens
                WHERE id_viagem = ?;
            '''

            self.cursor.execute(sql_deletar_viagem, (id_viagem,))
            self.conn.commit()
