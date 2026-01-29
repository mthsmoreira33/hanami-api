from fastapi import APIRouter, Query, HTTPException
from datetime import date
from hanami.db.connection import engine
from hanami.db.repository import SalesRepository
from hanami.services.search import build_search_filters

router = APIRouter(prefix="/data", tags=["Data"])

@router.get(
    "/search",
    summary="Busca genérica de vendas",
    description="Permite buscar vendas com múltiplos filtros opcionais."
)
def search_data(
    estado: str | None = Query(None, example="SP"),
    cidade: str | None = Query(None, example="São Paulo"),
    produto: str | None = Query(None, example="Notebook"),
    categoria: str | None = Query(None, example="Eletrônicos"),
    start_date: date | None = Query(None, example="2023-01-01"),
    end_date: date | None = Query(None, example="2023-12-31"),
    min_valor: float | None = Query(None, example=1000),
    max_valor: float | None = Query(None, example=5000),
    limit: int = Query(100, le=500),
):
    repo = SalesRepository(engine)

    filters = build_search_filters(
        estado,
        cidade,
        produto,
        categoria,
        start_date,
        end_date,
        min_valor,
        max_valor,
    )

    results = repo.search(filters, limit=limit)

    if not results:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")

    return {
        "total": len(results),
        "items": results
    }
