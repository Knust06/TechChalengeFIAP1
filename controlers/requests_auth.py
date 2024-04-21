import requests

class Autenticacao_Token:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "http://127.0.0.1:8000"
        self.token_url = f"{self.base_url}/token"
        try:
            self.token_response = self.get_token("teste", "teste")
        except requests.RequestException as e:
            print(f"Erro na autenticacao: {e}")

    def get_token(self, username, password, client_id='', client_secret=''):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = self.session.post(self.token_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
        
    def make_get(self, url):
        headers = {"Authorization": f"Bearer {self.token_response["access_token"]}"}
        response = requests.get(f"{self.base_url}{url}", headers=headers)
        return response
        
    def return_session(self):
        return self.session
