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
├── data/               # Dados de entrada e saída
│   ├── raw/            # Dados brutos (não versionados)
│   └── processed/      # Dados processados/artefatos
├── docs/               # Documentação adicional
├── src/
│   └── hanami/
│       ├── api/        # Camada HTTP (endpoints)
│       ├── core/       # Configuração, logs, versionamento
│       ├── models/     # Schemas Pydantic
│       ├── services/   # Regras de negócio e processamento
│       └── main.py     # Entry point da aplicação
├── tests/              # Testes automatizados
├── .gitignore
├── pyproject.toml
└── README.md
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

## 📘 Documentação da API

A documentação interativa (Swagger/OpenAPI) é gerada automaticamente pelo FastAPI:

- **Swagger UI:**
  ```
  http://localhost:8000/docs
  ```

- **OpenAPI JSON:**
  ```
  http://localhost:8000/openapi.json
  ```

---

## 🧪 Testes (opcional)

Para rodar os testes automatizados:

```bash
pytest
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