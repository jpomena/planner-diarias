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
        self.cursor.execute(gerar_tab_viagens)
        self.cursor.execute(gerar_tab_despesas)
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

    def add_despesas(self, despesas_viagem, nome_viagem_str):
        id_viagem = self.get_id(nome_viagem_str)
        self.del_despesas(id_viagem)

        sql_add_despesas = '''INSERT INTO despesas (
        data_despesa, tipo_despesa, loc_despesa, valor_despesa, id_viagem
        ) VALUES (?, ?, ?, ?, ?)
        '''
        for despesa in despesas_viagem:
            data = despesa['data']
            tipo = despesa['tipo']
            loc = despesa['loc']
            valor = despesa['valor']

            self.cursor.execute(
                sql_add_despesas, (
                    data, tipo, loc, valor, id_viagem
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

    def del_despesas(self, id_viagem):
        sql_delete_despesas = '''
            DELETE FROM despesas WHERE id_viagem = ?;
        '''
        self.cursor.execute(sql_delete_despesas, (id_viagem,))
        self.conn.commit()

    def get_despesas_por_nome(self, nome_viagem):
        id_viagem = self.get_id(nome_viagem)
        sql_despesas_viagem = '''
            SELECT data_despesa, tipo_despesa, loc_despesa, valor_despesa
            FROM despesas
            WHERE id_viagem = ?;
        '''
        self.cursor.execute(sql_despesas_viagem, (id_viagem,))
        resultados = self.cursor.fetchall()

        lista_despesas = []
        for resultado in resultados:
            dados_despesa = {
                'data': resultado[0],
                'tipo': resultado[1],
                'loc': resultado[2],
                'valor': resultado[3]
            }
            lista_despesas.append(dados_despesa)

        return lista_despesas

    def del_viagem(self, nome_viagem):
        id_viagem = self.get_id(nome_viagem)
        if id_viagem:
            sql_deletar_viagem = '''
                DELETE FROM viagens
                WHERE id_viagem = ?;
            '''

            self.cursor.execute(sql_deletar_viagem, (id_viagem,))
            self.conn.commit()
