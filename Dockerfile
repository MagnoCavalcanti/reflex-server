# Imagem base
FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório dentro do container
WORKDIR /app

# Copia apenas o requirements primeiro (melhora o cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas arquivos necessários
COPY app/ ./app/
COPY .env .env
COPY migrations ./migrations
COPY entrypoint.sh entrypoint.sh
COPY alembic.ini alembic.ini

# Porta do uvicorn (interna)
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
