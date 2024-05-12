from fastapi import FastAPI, Depends, HTTPException, status, Query
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, UTC
from scraper import Scraper

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

scraper = Scraper()

app = FastAPI(
    title="Embrapa Data API",
    description="API para consulta de dados de viticultura do site da Embrapa, incluindo produção, processamento, etc.",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    '''Cria um token de acesso JWT com os dados fornecidos.'''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", summary="Obtém o token de acesso", response_description="Token JWT para autenticação")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": user_token, "token_type": "bearer"}

@app.get("/data/production", tags=["Data Access"], summary="Acessa dados de produção",
         response_description="Dados de produção da viticultura")
async def production(year: Optional[int] = Query(None, description="Ano dos dados a serem recuperados"),token: str = Depends(oauth2_scheme)):
    try:
        data = scraper.get_production_data(year)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/processing", tags=["Data Access"], summary="Acessa dados de processamento",
         response_description="Dados de processamento da viticultura")
async def processing(year: Optional[int] = Query(None, description="Ano dos dados a serem recuperados"),token: str = Depends(oauth2_scheme)):
    try:
        data = scraper.get_processing_data(year)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/commercialization", tags=["Data Access"], summary="Acessa dados de comercialização",
         response_description="Dados de comercialização da viticultura")
async def commercialization(year: Optional[int] = Query(None, description="Ano dos dados a serem recuperados"),token: str = Depends(oauth2_scheme)):
    try:
        data = scraper.get_commercialization_data(year)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/importation", tags=["Data Access"], summary="Acessa dados de importação",
         response_description="Dados de importação da viticultura")
async def importation(year: Optional[int] = Query(None, description="Ano dos dados a serem recuperados"),token: str = Depends(oauth2_scheme)):
    try:
        data = scraper.get_importation_data(year)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/exportation", tags=["Data Access"], summary="Acessa dados de exportação",
         response_description="Dados de exportação da viticultura")
async def exportation(year: Optional[int] = Query(None, description="Ano dos dados a serem recuperados"),token: str = Depends(oauth2_scheme)):
    try:
        data = scraper.get_exportation_data(year)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

