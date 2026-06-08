#!/bin/bash
set -e

echo "🔄 Aguardando banco de dados..."
sleep 5

echo "🗃️ Executando migrations..."
alembic upgrade head

echo "🌱 Executando superpopulação do banco..."
python scripts/superpopulate_db.py

echo "🚀 Iniciando aplicação..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug