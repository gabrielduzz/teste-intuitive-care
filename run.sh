#!/bin/bash
echo "=========================================="
echo "  Iniciando Teste Intuitive Care - Pipeline ETL Completo"
echo "=========================================="

echo "[0/8] Limpando ambiente anterior..."
docker compose down -v

echo "[1/8] Subindo Banco de Dados..."
docker compose up -d

echo "[2/8] Aguardando Banco iniciar..."
sleep 10

echo "[3/8] Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "--- INICIANDO PIPELINE DE DADOS (ETL) ---"
echo ""

echo "[4/8] Etapa 1: Scraping de dados da ANS..."
python src/scraping.py
if [ $? -ne 0 ]; then
    echo "[AVISO] Falha no download ou site da ANS instavel."
    echo "Prosseguindo com dados locais se disponiveis..."
fi

echo "[5/8] Etapa 2: Processamento e Transformacao..."
python src/processing.py
python src/transformation.py
python src/join.py

echo "[6/8] Etapa 3: Validacao e Agregacao..."
python src/validation.py
python src/aggregation.py

echo "[7/8] Etapa 4: Importacao para o Banco de Dados..."
python src/import_data.py

echo ""
echo "=========================================="
echo "  Pipeline Finalizado!"
echo "  1. Backend: uvicorn backend.main:app --reload"
echo "  2. Frontend: cd frontend && npm run dev"
echo "=========================================="