# Previsão do Preço do Bitcoin com Machine Learning

Este projeto visa prever o preço do Bitcoin utilizando diferentes modelos de aprendizado de máquina. A previsão é baseada em dados históricos obtidos através da API do CoinGecko e técnicas como Lags e Média Móvel. Várias abordagens de modelagem foram aplicadas, como Regressão Linear, Ridge, Lasso, Gradient Boosting, XGBoost e Redes Neurais (MLP Regressor).

## Índice
1. [Coleta e Preparação dos Dados](#coleta-e-preparação-dos-dados)
2. [Modelos Utilizados](#modelos-utilizados)
3. [Otimização de Hiperparâmetros](#otimização-de-hiperparâmetros)
4. [Avaliação e Resultados](#avaliação-e-resultados)

---

## Coleta e Preparação dos Dados

### Coleta dos Dados
Os dados históricos de preço do Bitcoin foram obtidos a partir da API da CoinGecko, que fornece informações de mercado em USD.

```python
import requests
import pandas as pd

def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': '365',   # Coletando os últimos 365 dias
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Transformar os dados em um DataFrame
def prepare_data():
    data = get_bitcoin_data()
    prices = data['prices']

    # Criar DataFrame com timestamp e preço
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    return df

df = prepare_data()
