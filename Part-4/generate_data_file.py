import yfinance as yf
import json

# Configurações para coletar os dados de preços doBTC
symbol = 'BTC-USD'  # Símbolo da ação no Yahoo Finance
start_date = '2024-09-09'  # Data de início do histórico de preços
end_date = '2024-12-09'  # Data de fim do histórico de preços

# Baixa os dados históricos do BTC
df = yf.download(symbol, start=start_date, end=end_date)

# Verifica se o DataFrame possui a coluna 'Close' e não está vazio
if 'Close' in df.columns and not df['Close'].empty:
    # Extrai os preços de fechamento, remove valores ausentes e converte para uma lista de floats
    closing_prices = [float(price) for price in df['Close'].dropna().values]
    
    # Estrutura de dados no formato que a API espera
    data = {
        "prices": closing_prices
    }

    # Salva os dados no arquivo JSON
    file_name = 'closing_prices.json'
    with open(file_name, 'w') as file:
        json.dump(data, file)

    print(f"Arquivo '{file_name}' criado com sucesso no formato esperado pela API.")
else:
    print("Erro: Não foram encontrados dados válidos para a coluna 'Close'.")
