import requests
from bs4 import BeautifulSoup
import time

class Scraper():
    def get_data_from_url(self,url):
        max_retries = 10
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
        
    def get_categories(self, url):
        soup = self.get_data_from_url(url)
        categories = soup.find_all('button', attrs={'class':'btn_sopt'})
        categories= [category.text for category in categories]
        
        return categories

    def busca_tabelas(self, soup, year):
        
        data = []
        for row in soup.find('table', class_='tb_base tb_dados').find_all('tr'):
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            data.append(cols)

        cabe = data.pop(0)
        dict_teste = {}
        dict_content = {}

        for item in range(len(data[0])):
            dict_teste[cabe[item]] = []
        for item in data:
            for tam in range(len(item)):
                dict_teste[cabe[tam]].append(item[tam])

        dict_content[year] = dict_teste
        return dict_content

    def get_unique_table_content(self,soup,year):
            table = soup.find_all('table', attrs={'class': 'tb_base tb_dados'})
            contents = table[0].text.split('\n')
            contents = [item.strip() for item in contents]
            contents = [item for item in contents if item]
            if len(contents)>2:
                key_1 = contents[0]
                key_2 = contents[1]
                key_3 = contents[2]
                dict_content = {
                    'ano': year,
                    key_1:[],
                    key_2:[],
                    key_3:[]
                            }
                contents = contents[3:]

            
                for i in range(0, len(contents), 3):
                    dict_content[key_1].append(str(contents[i]))
                    if i+1 < len(contents):
                        dict_content[key_2].append(str(contents[i+1]))
                    if i+2 < len(contents):
                        dict_content[key_3].append(str(contents[i+2]))

            else:
                key_1 = contents[0]
                key_2 = contents[1]
                dict_content = {
                    'ano': year,
                    key_1:[],
                    key_2:[]
                            }
                contents = contents[2:]
                for i in range(0, len(contents), 2):
                    dict_content[key_1].append(str(contents[i]))

                for i in range(1, len(contents), 2):
                    if contents[i] == '-':
                        dict_content[key_2].append('null')
                    else:
                        dict_content[key_2].append(str(contents[i]))

            return dict_content
    
    def get_production_data(self, year_form=None):
        self.get_years()
        dict_content = {}
        for year in range(self.min_year, self.max_year+1):
            if year_form != None:
                if year == int(year_form):    
                    soup = self.get_data_from_url(f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02")
                    dict_content[year] = self.busca_tabelas(soup,year)[year]
            else:
                soup = self.get_data_from_url(f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02")
                dict_content[year] = self.busca_tabelas(soup,year)[year]
            
        return dict_content

    def get_processing_data(self, year_form=None):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
        self.get_years()
        categories = self.get_categories(url)
        dict_content = {}
        for num in range(0,len(categories)):
            dict_content.update({categories[num]: []})
            for year in range(self.min_year, self.max_year+1):
                if year_form != None:
                    if year == int(year_form):
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_0{num+1}"
                        soup = self.get_data_from_url(url)
                        dict_content[categories[num]].append(self.busca_tabelas(soup,year))
                else:
                    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_0{num+1}"
                    soup = self.get_data_from_url(url)
                    dict_content[categories[num]].append(self.busca_tabelas(soup,year))


        return dict_content

    def get_commercialization_data(self, year_form=None):
        self.get_years()
        dict_content = {}
        for year in range(self.min_year, self.max_year+1):
            if year_form != None:
                if year == int(year_form):
                    soup = self.get_data_from_url(f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04")
                    dict_content[year] = self.busca_tabelas(soup,year)[year]
            else:
                soup = self.get_data_from_url(f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04")
                dict_content[year] = self.busca_tabelas(soup,year)[year]


        return dict_content

    def get_importation_data(self, year_form=None):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05"
        self.get_years()
        categories = self.get_categories(url)
        dict_content = {}
        for num in range(0,len(categories)):
            dict_content.update({categories[num]: []})
            for year in range(self.min_year, self.max_year+1):
                if year_form != None:
                    if year == int(year_form):
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_0{num+1}"
                        soup = self.get_data_from_url(url)
                        dict_content[categories[num]].append(self.busca_tabelas(soup,year))
                else:
                    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_0{num+1}"
                    soup = self.get_data_from_url(url)
                    dict_content[categories[num]].append(self.busca_tabelas(soup,year))

        return dict_content

    def get_exportation_data(self, year_form=None):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
        self.get_years()
        categories = self.get_categories(url)
        dict_content = {}
        for num in range(0,len(categories)):
            dict_content.update({categories[num]: []})
            for year in range(self.min_year, self.max_year+1):
                if year_form != None:
                    if year == int(year_form):
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_0{num+1}"
                        soup = self.get_data_from_url(url)
                        dict_content[categories[num]].append(self.busca_tabelas(soup,year))
                else:
                    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_0{num+1}"
                    soup = self.get_data_from_url(url)
                    dict_content[categories[num]].append(self.busca_tabelas(soup,year))

        return dict_content

