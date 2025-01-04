from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import yfinance as yf
import joblib  # Para carregar o MinMaxScaler salvo

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
    start_date: str = "2024-09-09",
    end_date: str = "2024-12-09"
):
    """
    Faz o download dos preços históricos (coluna 'Close') de um determinado símbolo
    usando yfinance e retorna em formato JSON.
    Parâmetros query string (opcionais):
      - symbol (default BTC-USD)
      - start_date (default 2024-09-09)
      - end_date (default 2024-12-09)
    Exemplo de uso:
    GET /historical-prices?symbol=BTC-USD&start_date=2024-09-09&end_date=2024-12-09
    """
    df = yf.download(symbol, start=start_date, end=end_date)

    # Verifica se existe a coluna 'Close' e se não está vazia
    if "Close" not in df.columns or df["Close"].empty:
        raise HTTPException(
            status_code=404, detail=f"Nenhum dado válido encontrado para '{symbol}' nesse intervalo."
        )

    # Extrai os preços de fechamento, removendo valores ausentes
    closing_prices = [float(price) for price in df["Close"].dropna().values]

    # Retorna no formato JSON
    return {"prices": closing_prices}


#python -m uvicorn app:app --host 0.0.0.0 --port 8000
