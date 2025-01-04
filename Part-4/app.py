from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import yfinance as yf
import joblib
import pandas as pd
from datetime import date, datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

# Definir o modelo de dados para entrada
class StockData(BaseModel):
    prices: list[float]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (ajuste se necessário)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

model = tf.keras.models.load_model('lstm_model_bitcoin.keras')
scaler = joblib.load('scaler.save')  # Carrega o scaler usado no treinamento

@app.post("/predict-bitcoin")
async def predict(data: StockData):
    try:
        # Verifica o número de preços enviados
        ##if len(data.prices) < 60:
        ##    raise HTTPException(status_code=400, detail="A lista 'prices' deve conter pelo menos 60 valores.")

        # Prepara a entrada para o modelo (normaliza os dados de entrada para combinar com os dados de treinamento)
        input_data = np.array(data.prices).reshape(-1, 1)
        input_data_scaled = scaler.transform(input_data).reshape(1, -1, 1)

        # Faz a previsão
        prediction = model.predict(input_data_scaled)

        # Desnormaliza a previsão para obter o valor original
        prediction_real = scaler.inverse_transform(prediction)[0][0]

        return {"prediction": float(prediction_real)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-prices")
async def get_historical_prices(
    symbol: str = "BTC-USD",
    start_date: str = Query(None),  # Não define default direto, para tratar dinamicamente
    end_date: str = Query(None)
):
    """
    Faz o download dos preços históricos (coluna 'Close') de um determinado ticker
    usando yfinance e retorna no formato JSON.
    
    Parâmetros (query):
      - ticker: símbolo no Yahoo Finance (ex.: BTC-USD, AAPL, PETR4.SA)
      - start_date: data de início (YYYY-MM-DD)
      - end_date: data de fim (YYYY-MM-DD)
    
    Se o usuário não passar start_date e end_date,
    por padrão:
      - start_date = hoje - 60 dias
      - end_date = hoje
    Também verifica se o intervalo é >= 60 dias.
    """

    # Se o usuário não informar, define valores padrão
    if not start_date:
        start_date = (date.today() - timedelta(days=60)).isoformat()
    if not end_date:
        end_date = date.today().isoformat()

    # Converte strings para objeto date
    fmt = "%Y-%m-%d"
    try:
        start_date_obj = datetime.strptime(start_date, fmt).date()
        end_date_obj = datetime.strptime(end_date, fmt).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Datas devem estar no formato YYYY-MM-DD.")

    # Verifica se o intervalo é de pelo menos 60 dias
    diff_days = (end_date_obj - start_date_obj).days
    if diff_days < 60:
        raise HTTPException(
            status_code=400,
            detail=f"É necessário pelo menos 60 dias de intervalo. Intervalo atual: {diff_days} dias."
        )

    # Faz o download dos dados de 'Close' via yfinance
    df = yf.download(symbol, start=start_date, end=end_date)

    # Verifica se existe a coluna 'Close' e se não está vazia
    if "Close" not in df.columns or df["Close"].empty:
        raise HTTPException(
            status_code=404, 
            detail=f"Nenhum dado válido encontrado para '{symbol}' no intervalo {start_date} a {end_date}."
        )

    # Extrai os preços de fechamento, removendo valores ausentes
    closing_prices = [float(price) for price in df["Close"].dropna().values]

    # Retorna no formato JSON
    return {"prices": closing_prices}

@app.post("/prices-info")
async def get_price_info(data: StockData):
    """
Recebe uma lista de preços e retorna agregações úteis, como:

- Média:
    - Uma métrica que pode nos ajudar a entender a tendência central dos preços ao longo do período analisado.

- Valor mínimo e máximo:
    - Identifica o menor e o maior valor na lista, permitindo entender os limites de variação do preço.

- Desvio padrão:
    - Ajuda a compreender a variabilidade dos preços ao longo do tempo, indicando o nível de volatilidade.

- Range (diferença entre máximo e mínimo):
    - Mede a amplitude de variação dos preços, mostrando o intervalo entre o maior e o menor valor.

- Mediana:
    - Representa o valor central dos preços ordenados, sendo menos sensível a valores extremos (outliers).

- Preço inicial e final:
    - Representam os preços no início e no fim do período analisado, fornecendo um panorama do desempenho.

- Retorno total:
    - Calcula a variação percentual entre o preço inicial e final, indicando o ganho ou perda acumulada.

- Retorno médio diário:
    - Mede a rentabilidade média diária ao longo do período.

- Volatilidade:
    - Representa o desvio padrão dos retornos diários, indicando o nível de risco do ativo.

- Momentum:
    - Mostra a diferença entre o preço atual e o de 10 períodos atrás, indicando a força da tendência recente.
"""
    try:
        prices = data.prices

        if not prices:
            raise HTTPException(status_code=400, detail="A lista 'prices' não pode estar vazia.")

        # Função de agregação
        def calculate_aggregations(prices: list[float]) -> dict:
            daily_returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
            return {
                "average_price": sum(prices) / len(prices),
                "min_price": min(prices),
                "max_price": max(prices),
                "price_range": max(prices) - min(prices),
                "std_dev": np.std(prices),
                "median_price": np.median(prices),
                "initial_price": prices[0],
                "final_price": prices[-1],
                "total_return": ((prices[-1] - prices[0]) / prices[0]) * 100,                
                "average_daily_return": sum(daily_returns) / len(daily_returns),
                "volatility": np.std(daily_returns),
                "momentum": prices[-1] - prices[-10]  # Diferença entre último preço e preço 10 períodos atrás
            }

        # Calcula as agregações
        aggregations = calculate_aggregations(prices)

        return {"prices_info": aggregations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/tickers")
async def get_tickers():
    """
    Retorna a lista de tickers brasileiros disponíveis no formato utilizado pelo yfinance.
    """
    def obter_tickers_de_repositorio():
        try:
            url = "https://raw.githubusercontent.com/leomaurodesenv/b3-stock-indexes/main/output/stock-indexes.csv"
            df = pd.read_csv(url)
            tickers = df['Code'].apply(lambda x: f"{x}.SA").tolist()
            return tickers
        except Exception as e:
            raise Exception(f"Erro ao obter tickers: {str(e)}")
    
    try:    
        tickers = obter_tickers_de_repositorio()
        if not tickers:
            raise HTTPException(status_code=404, detail="Nenhum ticker encontrado.")
        return {"tickers": tickers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#python -m uvicorn app:app --host 0.0.0.0 --port 8080
