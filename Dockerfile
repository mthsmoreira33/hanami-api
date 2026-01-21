FROM python:3.11-slim

# Evita bytecode e buffering estranho
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

# Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Porta da API
EXPOSE 8000

# Start da aplicação
CMD ["uvicorn", "hanami.main:app", "--host", "0.0.0.0", "--port", "8000"]
