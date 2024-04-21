import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlers.requests_auth import Autenticacao_Token

Autenticacao = Autenticacao_Token()

teste = Autenticacao.make_get("/data/production")

print(teste)