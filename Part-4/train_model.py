import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib

# Configurações para coletar os dados de preços do BTC
symbol = 'BTC-USD'
start_date = '2013-01-01'
end_date = '2024-11-29'

# Baixar dados históricos da ação
df = yf.download(symbol, start=start_date, end=end_date)

# Verificar se o DataFrame possui a coluna 'Close' e não está vazio
if 'Close' in df.columns and not df['Close'].empty:
    # Configura e ajusta o scaler para normalizar os dados
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['Close'] = scaler.fit_transform(df[['Close']])

    # Salva o scaler para ser usado na API durante a desnormalização
    joblib.dump(scaler, 'scaler.save')

    # Função para criar sequências para o modelo LSTM
    def create_sequences(data, seq_length=60):
        x, y = [], []
        for i in range(len(data) - seq_length):
            x.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(x), np.array(y)

    # Dividir os dados em treino e teste
    train_size = int(len(df) * 0.8)
    train_data, test_data = df['Close'].values[:train_size], df['Close'].values[train_size:]
    x_train, y_train = create_sequences(train_data)
    x_test, y_test = create_sequences(test_data)

    # Ajuste das dimensões dos dados para o LSTM
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Construir o modelo LSTM
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])

    # Compilar o modelo
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Treinar o modelo
    model.fit(x_train, y_train, batch_size=64, epochs=75, validation_data=(x_test, y_test))

    # Salvar o modelo treinado
    model.save('lstm_model_bitcoin.h5')
    print("Modelo treinado e salvo com sucesso!")
else:
    print("Erro: Não foram encontrados dados válidos para a coluna 'Close'.")
