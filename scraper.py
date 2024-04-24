import requests
from bs4 import BeautifulSoup
import re
import time

class Scraper():
    def get_data_from_url(self,url):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                '''Pega o conteúdo de uma página web e retorna o texto dela.'''
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')

                return soup 
            except requests.exceptions.RequestException as e:
                print(f'Erro ao buscar a URL {url}: {e}')
                retries += 1
                time.sleep(1)

    def get_years(self):
        soup = self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")
        years = soup.find_all('label', attrs={'class': 'lbl_pesq'})
        self.min_year = int(years[0].text[-11:-7])
        self.max_year = int(years[0].text[-6:-2])
        
    def get_apresentacao_data(self):
        return self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01")

    def get_production_data(self):
        for year in range(self.min_year, self.max_year+1):
            soup = self.get_data_from_url(f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02")
            table = soup.find_all('table', attrs={'class': 'tb_base tb_dados'})
            contents = table[0].text.split('\n')
            contents = [item.strip() for item in contents]
            contents = [item for item in contents if item]
            key_1 = contents[0]
            key_2 = contents[1]
            dict_prod = {
                'ano': year,
                key_1:[],
                key_2:[]
                        }
            contents = contents[2:]
            for i in range(0, len(contents), 2):
                dict_prod[key_1].append(str(contents[i]))

            for i in range(1, len(contents), 2):
                if contents[i] == '-':
                    dict_prod[key_2].append('null')
                else:
                    dict_prod[key_2].append(str(contents[i]))

            print(dict_prod)

        return 

    def get_processing_data(self):
        return self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03")

    def get_commercialization_data(self):
        return self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04")

    def get_importation_data(self):
        return self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05")

    def get_exportation_data(self):
        return self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06")

    def get_publication_data(self):
        return self.get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_07")

scraper = Scraper()
scraper.get_years()
scraper.get_production_data()