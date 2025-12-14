from fastapi import FastAPI
from hanami.api.router import router as api_router
from hanami.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Hanami API",
    version="0.1.0",
)

app.include_router(api_router)