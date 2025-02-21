# Usar uma imagem base com Python 3.9
FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    fastapi==0.78.0 uvicorn==0.18.2

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    tensorflow yfinance

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    numpy==1.21.6 scikit-learn==1.0.2

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    pydantic==1.9.1 scipy==1.8.1

RUN pip install --no-cache-dir --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ \
    pandas==1.5.0 

ENV CUDA_VISIBLE_DEVICES=""

COPY . .

# Exponha a porta 8000 dentro do container
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
