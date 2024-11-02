# Usar uma imagem base com Python 3.9
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Atualiza o pip para a versão mais recente
RUN pip install --upgrade pip

# Instala dependências em blocos, com timeout e espelho alternativo
RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    fastapi==0.78.0 uvicorn==0.18.2

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    tensorflow==2.9.1 yfinance==0.1.70

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    numpy==1.21.6 scikit-learn==1.0.2

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    pydantic==1.9.1 scipy==1.8.1

# Copia o restante do código para o container
COPY . .

# Comando para iniciar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
