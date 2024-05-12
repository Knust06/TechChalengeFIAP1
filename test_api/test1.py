import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import Scraper
from db_utils import DB_utils
from controlers.requests_auth import Autenticacao_Token

scraper = Scraper()
Autenticacao = Autenticacao_Token()

dbsession = DB_utils()

teste = Autenticacao.make_get("/data/exportation?year=2023")

print(teste)