from pathlib import Path
from sqlalchemy import create_engine

DB_PATH = Path("data/processed/hanami.db")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    future=True
)
