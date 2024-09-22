# Previsão do Preço do Bitcoin com Machine Learning

Este projeto visa prever o preço do Bitcoin utilizando diferentes modelos de aprendizado de máquina. A previsão é baseada em dados históricos obtidos através da API do CoinGecko e técnicas como Lags e Média Móvel. Várias abordagens de modelagem foram aplicadas, como Regressão Linear, Ridge, Lasso, Gradient Boosting, XGBoost e Redes Neurais (MLP Regressor).

## Índice
1. [Coleta e Preparação dos Dados](#coleta-e-preparação-dos-dados)
2. [Modelos Utilizados](#modelos-utilizados)
3. [Otimização de Hiperparâmetros](#otimização-de-hiperparâmetros)
4. [Avaliação e Resultados](#avaliação-e-resultados)
5. [Escolha Modelos](#escolha-modelos)
6. [Conclusão](#conclusão)

---

## Coleta e Preparação dos Dados

### Coleta dos Dados
Os dados históricos de preço do Bitcoin foram obtidos a partir da API da CoinGecko, que fornece informações de mercado de cripto.

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
```

### Preparação dos Dados
Na preparação dos dados, foram criadas variáveis de lag para os últimos 1 e 7 dias, além de uma média móvel de 7 dias, para capturar tendências de curto prazo.

```python
def create_features(df):
    # Criando lag de 1 e 7 dias e uma média móvel de 7 dias
    df['lag_1'] = df['price'].shift(1)
    df['lag_7'] = df['price'].shift(7)
    df['ma_7'] = df['price'].rolling(window=7).mean()

    # Remover valores nulos
    df = df.dropna()
    return df

df_features = create_features(df)

# Definir variáveis X (features) e y (target)
X = df_features[['lag_1', 'lag_7', 'ma_7']]
y = df_features['price']

# Dividir o conjunto de dados em treino e teste
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

```
---

## Modelos Utilizados
Utilizamos uma variedade de modelos de aprendizado de máquina para prever o preço do Bitcoin.

### Regressão Linear

```python
from sklearn.linear_model import LinearRegression

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)


```

### Ridge e Lasso

```python
from sklearn.linear_model import Ridge, Lasso

ridge_model = Ridge(alpha=0.1)
ridge_model.fit(X_train, y_train)

lasso_model = Lasso(alpha=0.1, max_iter=1000)
lasso_model.fit(X_train, y_train)

```

### Gradient Boosting e XGBoost

```python
from sklearn.ensemble import GradientBoostingRegressor
import xgboost as xgb

gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
gb_model.fit(X_train, y_train)

xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
xgb_model.fit(X_train, y_train)

```

### Gradient Boosting e XGBoost

```python
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

# Padronizar os dados
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar a Rede Neural
nn_model = MLPRegressor(hidden_layer_sizes=(100,), activation='relu', solver='adam', max_iter=1000)
nn_model.fit(X_train_scaled, y_train)

```

---

## Otimização de Hiperparâmetros
Testamos diferentes combinações de hiperparâmetros para os modelos Ridge, Lasso, Gradient Boosting, XGBoost e MLP. Abaixo está um exemplo de otimização para o Ridge.

```python
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge

alphas = [0.01, 0.1, 1.0]
solvers = ['auto', 'svd', 'cholesky']

ridge_metrics = {}

for alpha in alphas:
    for solver in solvers:
        ridge_model = Ridge(alpha=alpha, solver=solver)
        ridge_model.fit(X_train, y_train)
        y_pred = ridge_model.predict(X_test)
        ridge_metrics[(alpha, solver)] = {
            'MSE': mean_squared_error(y_test, y_pred),
            'R²': r2_score(y_test, y_pred)
        }

# Melhor modelo baseado no MSE
best_ridge_params = min(ridge_metrics, key=lambda k: ridge_metrics[k]['MSE'])
print("Melhores parâmetros para Ridge:", best_ridge_params)

```
O mesmo processo de otimização foi aplicado para os outros modelos, como Lasso, Gradient Boosting, XGBoost e MLP.

---

## Avaliação e Resultados

Os resultados foram avaliados utilizando as seguintes métricas:

- **MSE**: Mean Squared Error
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error
- **R²**: Coeficiente de Determinação
- **MAPE**: Mean Absolute Percentage Error

### Previsão para o Próximo Dia

Após o treinamento e ajuste dos modelos, utilizamos o último dia de dados para prever o preço do Bitcoin no dia seguinte.

```python
last_row = df_features.iloc[-1]

# Preparar os dados para a previsão
new_data = [[last_row['lag_1'], last_row['lag_7'], last_row['ma_7']]]

# Prever o preço com cada modelo
tomorrow_price_linear = linear_model.predict(new_data)
tomorrow_price_ridge = ridge_model.predict(new_data)
tomorrow_price_lasso = lasso_model.predict(new_data)
tomorrow_price_gb = gb_model.predict(new_data)
tomorrow_price_xgb = xgb_model.predict(new_data)
tomorrow_price_nn = nn_model.predict(new_data)

# Resultados
print(f"Previsão do preço do Bitcoin para amanhã (Linear): {tomorrow_price_linear[0]:.2f}")
print(f"Previsão do preço do Bitcoin para amanhã (Ridge): {tomorrow_price_ridge[0]:.2f}")
print(f"Previsão do preço do Bitcoin para amanhã (Lasso): {tomorrow_price_lasso[0]:.2f}")
print(f"Previsão do preço do Bitcoin para amanhã (Gradient Boosting): {tomorrow_price_gb[0]:.2f}")
print(f"Previsão do preço do Bitcoin para amanhã (XGBoost): {tomorrow_price_xgb[0]:.2f}")
print(f"Previsão do preço do Bitcoin para amanhã (MLP): {tomorrow_price_nn[0]:.2f}")
'''
```
---
##Escolha Modelos 

**Ridge Regression** e **Lasso Regression** são os dois melhores modelo para essas previsão, e aqui estão os motivos:

###Vantagens do Ridge e Lasso
Regularização: Tanto o Ridge quanto o Lasso utilizam técnicas de regularização que ajudam a prevenir o overfitting, ou seja, quando o modelo se ajusta excessivamente aos dados de treinamento. Isso é crucial em dados financeiros, onde ruídos podem distorcer as previsões.

###Métricas de Desempenho:

Apesar da leve diferença entre os dois, ambos os modelos estão em uma faixa de erro bastante competitiva.
Embora Ridge e Lasso compartilhem a mesma base teórica de regularização, eles diferem em como aplicam essa regularização:

Ridge Regression utiliza a regularização L2, que adiciona uma penalização proporcional ao quadrado dos coeficientes. Isso significa que o Ridge tende a incluir todas as variáveis no modelo, mas com coeficientes menores. Isso pode ser benéfico quando muitas variáveis têm relevância, pois preserva a informação.

Lasso Regression, por outro lado, utiliza a regularização L1, que penaliza a soma dos valores absolutos dos coeficientes. Isso pode levar a uma seleção de variáveis, onde algumas são reduzidas a zero. O Lasso é, portanto, útil quando se busca um modelo mais simples, com menos variáveis, que ainda consiga manter uma boa precisão nas previsões.

---
##Conclusão
A escolha entre Ridge e Lasso depende do contexto da análise. Para este teste específico, ambos os modelos demonstraram-se eficazes e robustos, proporcionando boas previsões para o preço do Bitcoin. Enquanto o Ridge é ideal para manter todas as variáveis no modelo, o Lasso oferece uma abordagem mais focada, potencialmente melhor para interpretação. Juntos, eles representam uma forte combinação de técnicas de regressão que podem ser valiosas em diferentes cenários de análise de dados.
