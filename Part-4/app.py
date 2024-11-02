from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
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

#python -m uvicorn app:app --host 0.0.0.0 --port 8000
