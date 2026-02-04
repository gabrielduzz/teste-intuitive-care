@echo off
echo ==========================================
echo   Iniciando Teste Intuitive Care - Pipeline ETL Completo
echo ==========================================

echo [0/8] Limpando ambiente anterior...
docker compose down -v

echo [1/8] Subindo Banco de Dados...
docker compose up -d

echo [2/8] Aguardando Banco iniciar (10s)...
timeout /t 10

echo [3/8] Instalando dependencias...
pip install -r requirements.txt

echo.
echo --- INICIANDO PIPELINE DE DADOS (ETL) ---
echo.

echo [4/8] Etapa 1: Scraping de dados da ANS...
python scraping.py
if %errorlevel% neq 0 (
    echo [AVISO] Falha no download. Verifique sua internet ou o site da ANS.
    echo Tentando usar dados locais caso existam...
)

echo [5/8] Etapa 2: Processamento e Transformacao...
python processing.py
python transformation.py
python join.py

echo [6/8] Etapa 3: Validacao e Agregacao...
python validation.py
python aggregation.py

echo [7/8] Etapa 4: Importacao para o Banco de Dados...
python import_data.py

echo.
echo ==========================================
echo   Pipeline Finalizado!
echo   
echo   Para rodar a aplicacao:
echo   1. Backend: uvicorn backend.main:app --reload
echo   2. Frontend: cd frontend && npm run dev
echo ==========================================
pause