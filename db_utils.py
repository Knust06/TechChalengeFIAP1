from sqlalchemy import create_engine, MetaData, Table, text
import json
from crypts import descriptogradar
class DB_utils:
    def __init__(self):
        with open('credential.json', 'r') as arquivo:
            credenciais = json.load(arquivo)
        self.engine = create_engine(f"postgresql://{credenciais['sql_user']}:{descriptogradar(credenciais['fernet'].encode(),credenciais['sql_pass'])}@pg-12909575-fiap-data.k.aivencloud.com:11423/defaultdb?sslmode=require")
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.tables = {}

    def query(self, sql_query):
        if not self.connection:
            raise ValueError("Connection is not established. Call connect() method first.")
        
        query = text(sql_query)
        result = self.connection.execute(query)
        return result.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def carga_tabela(self, tabela_nome, data):
        if tabela_nome not in self.tables:
            self.tables[tabela_nome] = Table(tabela_nome, self.metadata, autoload_with=self.engine)

        inserir = self.tables[tabela_nome].insert()

        self.connection.execute(inserir, data)

        self.connection.commit()

    def limpar_tabela(self, table_name):
        if table_name not in self.tables:
            self.tables[table_name] = Table(table_name, self.metadata, autoload_with=self.engine)

        deletar = self.tables[table_name].delete()

        self.connection.execute(deletar)

        self.connection.commit()
