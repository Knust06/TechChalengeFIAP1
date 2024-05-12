import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import Scraper
from db_utils import DB_utils
from controlers.requests_auth import Autenticacao_Token

scraper = Scraper()
Autenticacao = Autenticacao_Token()

dbsession = DB_utils()

dbsession.limpar_tabela("tbl_processamento")

data = scraper.get_processing_data()

data_append = []

for item in data:
    for lista in data[item]:
        for index in range(len(lista[list(lista)[0]][list(lista[list(lista)[0]])[0]])):
            if lista[list(lista)[0]]["Quantidade (Kg)"][index] == "-" or lista[list(lista)[0]]["Quantidade (Kg)"][index] == "nd" or lista[list(lista)[0]]["Quantidade (Kg)"][index] == "*":
                data_append.append({"ano":list(lista)[0], "tipo":item,"cultivar":lista[list(lista)[0]][list(lista[list(lista)[0]])[0]][index], "quantidade":0})
            else:
                data_append.append({"ano":list(lista)[0], "tipo":item,"cultivar":lista[list(lista)[0]][list(lista[list(lista)[0]])[0]][index], "quantidade":float(lista[list(lista)[0]][list(lista[list(lista)[0]])[1]][index].replace(".", ""))})

dbsession.carga_tabela("tbl_processamento", data_append)

dbsession.close()