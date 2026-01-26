from fastapi import APIRouter, Query, HTTPException
from hanami.db.connection import engine
from hanami.db.repository import SalesRepository
from hanami.services.analytics import sales_trends

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get(
    "/trends",
    summary="Análise de tendências temporais",
    description="Retorna a evolução das vendas ao longo do tempo."
)
def trends(
    freq: str = Query(
        default="M",
        description="Frequência temporal: D (dia), M (mês), Y (ano)",
        enum=["D", "M", "Y"]
    )
):
    repo = SalesRepository(engine)
    df = repo.fetch_dataframe()

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado disponível")

    try:
        return sales_trends(df, freq=freq)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
