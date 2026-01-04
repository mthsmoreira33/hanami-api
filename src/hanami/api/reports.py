from fastapi import APIRouter, HTTPException, Query
from loguru import logger

from hanami.db.connection import engine
from hanami.db.repository import SalesRepository
from hanami.services.analytics import calculate_sales_metrics, calculate_product_analysis, calculate_financial_metrics

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/sales-summary")
def get_sales_summary():
    try:
        repo = SalesRepository(engine)
        df = repo.fetch_all()

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado de vendas disponível"
            )

        sales_metrics = calculate_sales_metrics(df)
        return sales_metrics

    except HTTPException:
        raise

    except Exception:
        logger.exception("Erro ao gerar resumo de vendas")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar resumo de vendas"
        )

@router.get("/product-analysis")
def product_analysis(
    sort_by: str | None = Query(
        default=None,
        description="Campo para ordenação: quantidade_vendida ou total_arrecadado"
    )
):
    try:
        repo = SalesRepository(engine)
        df = repo.fetch_dataframe()

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado de vendas disponível"
            )

        products = calculate_product_analysis(df)

        if sort_by:
            if sort_by not in {"quantidade_vendida", "total_arrecadado"}:
                raise HTTPException(
                    status_code=400,
                    detail="Parâmetro sort_by inválido"
                )
            products = sorted(
                products,
                key=lambda x: x[sort_by],
                reverse=True
            )

        return products

    except HTTPException:
        raise

    except Exception:
        logger.exception("Erro ao gerar análise de produtos")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar análise de produtos"
        )

@router.get("/financial-metrics")
def financial_metrics():
    try:
        repo = SalesRepository(engine)
        df = repo.fetch_dataframe()

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado de vendas disponível"
            )

        metrics = calculate_financial_metrics(df)

        return metrics

    except HTTPException:
        raise

    except Exception:
        logger.exception("Erro ao gerar métricas financeiras")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar métricas financeiras"
        )