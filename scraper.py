import requests
from bs4 import BeautifulSoup

def get_data_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.text  

def get_apresentacao_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01")

def get_production_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")

def get_processing_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03")

def get_commercialization_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04")

def get_importation_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05")

def get_exportation_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06")

def get_publication_data():
    return get_data_from_url("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_07")