import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import Scraper
from db_utils import DB_utils
from controlers.requests_auth import Autenticacao_Token

scraper = Scraper()
Autenticacao = Autenticacao_Token()

dbsession = DB_utils()

dbsession.limpar_tabela("tbl_exportacao")

data = scraper.get_exportation_data()

data_append = []

for tipo in data:
    for item in data[tipo]:
        for index in range(len(item["Países"])):
            if item["Quantidade (Kg)"][index] == "-":
                data_append.append({"ano":item["ano"], "tipo":tipo,"pais":item["Países"][index], "quantidade":0, "valor": 0})
            else:
                data_append.append({"ano":item["ano"], "tipo":tipo,"pais":item["Países"][index], "quantidade":int(item["Quantidade (Kg)"][index].replace(".","")), "valor": item["Valor (US$)"][index].replace(".","")})
        
dbsession.carga_tabela("tbl_exportacao", data_append)

dbsession.close()