from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import yfinance as yf
import joblib
from datetime import date, datetime, timedelta

# Definir o modelo de dados para entrada
class StockData(BaseModel):
    prices: list[float]

app = FastAPI()
model = tf.keras.models.load_model('lstm_model_bitcoin.h5')
scaler = joblib.load('scaler.save')  # Carrega o scaler usado no treinamento

@app.post("/predict")
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


#python -m uvicorn app:app --host 0.0.0.0 --port 8000
