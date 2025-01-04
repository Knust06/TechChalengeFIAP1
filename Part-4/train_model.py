import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib

# Importar callbacks e métricas que você usa
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.optimizers import Adam

# ==========================
# 1) COLETAR E PREPARAR OS DADOS
# ==========================
# Configurações para coletar os dados de preços do BTC
symbol = 'BTC-USD'
start_date = '2024-02-01'
end_date = '2025-01-02'

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

    # Caso o test_data seja curto demais para gerar sequências, pode dar shape (0,...). Verifique:
    if x_test.shape[0] == 0:
        print("Aviso: Não há dados suficientes para test_data com seq_length=60. Ajuste datas ou seq_length.")
        # Dependendo do caso, você pode interromper aqui ou seguir com apenas treino.
        exit()

    # ==========================
    # 2) CONSTRUIR E COMPILAR O MODELO
    # ==========================
    model = Sequential([
    # Primeira camada LSTM com return_sequences=True para empilhar outra LSTM
    LSTM(64, return_sequences=True, input_shape=(x_train.shape[1], 1)),
    Dropout(0.2),
    
    # Segunda camada LSTM, sem return_sequences porque é a última LSTM
    LSTM(64, return_sequences=False),
    Dropout(0.2),
    
    # Camadas densas para refinar
    Dense(32, activation='relu'),
    Dense(1)  # Saída única (preço previsto)
    ])

    # Compilar o modelo
    model.compile(optimizer='adam', loss='mean_squared_error')
    # ==========================
    # 3) TREINAR O MODELO COM CALLBACKS
    # ==========================
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,             # Número de épocas sem melhorar para interromper
        restore_best_weights=True  # Restaura os pesos da melhor época
    )

    checkpoint = ModelCheckpoint(
        'lstm_model_bitcoin.keras',         # Salva o modelo em cada melhora de val_loss
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )

    history = model.fit(
        x_train, y_train,
        validation_data=(x_test, y_test),
        epochs=100,
        batch_size=64,
        callbacks=[early_stop, checkpoint]
    )
    # Compilar o modelo

    # ==========================
    # 4) AVALIAR E SALVAR O MODELO
    # ==========================
    # Se preferir, salve sempre o último estado treinado:
    model.save('modelo_final.h5')
    print("Modelo final salvo em 'modelo_final.h5'.")

    # Métricas no conjunto de teste
    if x_test.shape[0] > 0:
        y_pred_scaled = model.predict(x_test)
        y_pred = scaler.inverse_transform(y_pred_scaled)             # Desnormaliza predições
        y_test_ = scaler.inverse_transform(y_test.reshape(-1, 1))    # Desnormaliza alvos
        
        rmse = np.sqrt(mean_squared_error(y_test_, y_pred))
        mae = mean_absolute_error(y_test_, y_pred)
else:
    print("Erro: Não foram encontrados dados válidos para a coluna 'Close'.")
