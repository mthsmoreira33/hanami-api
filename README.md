# Hanami API

API de análise de dados construída com **FastAPI** e **Pandas**, focada em ingestão de arquivos CSV/XLSX e geração de relatórios analíticos.

O objetivo principal deste projeto é fornecer uma base reprodutível e organizada para processamento, validação e análise de dados de vendas.

---

## 📌 Requisitos

- Python **3.10+**
- Git

> Recomenda-se fortemente o uso de ambiente virtual (`venv`).

---

## 📁 Estrutura do Projeto

```text
hanami-api/
├── .venv/
├── data/
│   ├── processed/
│   └── raw/
├── docs/
├── logs/
├── scripts/
│   ├── check_analytics.py
│   ├── check_db.py
│   └── check_ingestion.py
├── src/
│   └── hanami/
│       ├── api/
│       │   ├── __init__.py
│       │   ├── analytics.py
│       │   ├── data.py
│       │   ├── reports.py
│       │   ├── router.py
│       │   └── upload.py
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   ├── storage.py
│       │   └── versioning.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   └── repository.py
│       ├── models/
│       │   ├── reports.py
│       │   └── schemas.py
│       └── services/
│           ├── __init__.py
│           ├── analytics.py
│           ├── ingestion.py
│           ├── search.py
│           └── validation.py
├── tests/
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## ⚙️ Setup do Ambiente

### 1️⃣ Clonar o repositório

```bash
git clone <url-do-repositorio>
cd hanami-api
```

---

### 2️⃣ Criar e ativar o ambiente virtual

**Linux / macOS**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3️⃣ Instalar as dependências

Instalação do projeto em modo editável, incluindo dependências de desenvolvimento:

```bash
pip install -e .[dev]
```

Isso fará o `pip`:

- ler o `pyproject.toml`
- instalar todas as dependências necessárias
- tornar o pacote `hanami` importável

---

## ▶️ Executando o Projeto

Com o ambiente virtual ativo:

```bash
uvicorn hanami.main:app --reload
```

A API estará disponível em:

```
http://localhost:8000
```

---

## 🐳 Executando com Docker

Se preferir rodar via Docker:

1. **Construir e subir o container**

```bash
docker-compose up --build -d
```

A API estará disponível em:

```
http://localhost:8000
```

---

## 📘 Documentação da API

A documentação interativa (Swagger/OpenAPI) é gerada automaticamente pelo FastAPI:

**Swagger UI**
```
http://localhost:8000/docs
```

**OpenAPI JSON**
```
http://localhost:8000/openapi.json
```

---

## 📝 Observações Importantes

- O diretório `data/raw/` é ignorado pelo Git e deve conter apenas dados locais.
- Artefatos gerados podem ser salvos em `data/processed/`.
- Configurações sensíveis devem ser definidas via variáveis de ambiente (`.env`).

---

## ✅ Critérios de Aceite Atendidos

- Repositório Git inicializado e `.gitignore` configurado
- Estrutura de pastas definida
- README com instruções claras de instalação e execução

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT.
