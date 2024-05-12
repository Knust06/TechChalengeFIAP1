import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import Scraper
from db_utils import DB_utils
from controlers.requests_auth import Autenticacao_Token

scraper = Scraper()
Autenticacao = Autenticacao_Token()

dbsession = DB_utils()

dbsession.limpar_tabela("tbl_comercializacao")

data = scraper.get_commercialization_data()

data_append = []

for item in data:
    for index in range(len(data[item][list(data[item])[0]])):
        if data[item]["Quantidade (L.)"][index] == "-" or data[item]["Quantidade (L.)"][index] == "nd" or data[item]["Quantidade (L.)"][index] == "*":
            data_append.append({"ano":item, "produto":data[item]["Produto"][index],"quantidade":0})
        else:
            data_append.append({"ano":item, "produto":data[item]["Produto"][index],"quantidade":float(data[item]["Quantidade (L.)"][index].replace(".", ""))})

dbsession.carga_tabela("tbl_comercializacao", data_append)

dbsession.close()