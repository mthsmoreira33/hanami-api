from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from pathlib import Path
from hanami.db.connection import engine
from hanami.db.repository import SalesRepository
from hanami.services.analytics import calculate_sales_metrics, calculate_product_analysis, calculate_financial_metrics, metrics_by_region, demographic_distribution
from fastapi.responses import FileResponse
from fastapi import Query
from typing import Optional
from datetime import date
import pandas as pd
import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from typing import Literal
from hanami.models.reports import (
    SalesSummaryResponse,
    ProductAnalysisItem,
    FinancialMetricsResponse,
    RegionalPerformanceResponse,
    CustomerProfileResponse,
)

router = APIRouter(prefix="/reports", tags=["Reports"])

REPORTS_DIR = Path("data/processed/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

@router.get(
    "/sales-summary",
    summary="Resumo de vendas",
    description="Retorna métricas agregadas de vendas, com filtro opcional por período."
)
def get_sales_summary(
    start_date: Optional[date] = Query(
        default=None,
        description="Data inicial no formato YYYY-MM-DD"
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="Data final no formato YYYY-MM-DD"
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

        # 🔹 Conversão explícita (essencial)
        df["data_venda"] = pd.to_datetime(df["data_venda"])

        # 🔹 Aplicação dos filtros
        if start_date:
            df = df[df["data_venda"] >= pd.Timestamp(start_date)]

        if end_date:
            df = df[df["data_venda"] <= pd.Timestamp(end_date)]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma venda encontrada no período informado"
            )

        return calculate_sales_metrics(df)

    except HTTPException:
        raise

    except Exception:
        logger.exception("Erro ao gerar resumo de vendas")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar resumo de vendas"
        )

@router.get(
    "/product-analysis",
    response_model=list[ProductAnalysisItem],
    summary="Análise de vendas por produto",
    description="Retorna métricas agregadas por produto com opção de ordenação."
)
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

@router.get(
    "/financial-metrics",
    response_model=FinancialMetricsResponse,
    summary="Métricas financeiras",
    description="Retorna receita líquida, custo total e lucro bruto."
)
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


@router.get(
    "/regional-performance",
    summary="Performance regional",
    description="Retorna métricas agregadas por região, com filtro opcional por estado."
)
def regional_performance(
    estado: Optional[str] = Query(
        default=None,
        description="Filtra os dados por estado (ex: SP, RJ, MG)"
    )
):
    try:
        repo = SalesRepository(engine)
        df = repo.fetch_dataframe()

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado disponível"
            )

        if estado:
            df = df[df["estado_cliente"] == estado]

            if df.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"Nenhum dado encontrado para o estado {estado}"
                )

        regional_df = metrics_by_region(df)

        return (
            regional_df
            .round(2)
            .set_index("regiao")
            .to_dict(orient="index")
        )

    except HTTPException:
        raise
    except Exception:
        logger.exception("Erro ao gerar performance regional")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar performance regional"
        )

@router.get(
    "/customer-profile",
    response_model=CustomerProfileResponse,
    summary="Perfil demográfico dos clientes",
    description="Retorna distribuições demográficas dos clientes como gênero, faixa etária, cidade, estado e região."
)
def customer_profile():
    try:
        repo = SalesRepository(engine)
        df = repo.fetch_dataframe()

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado disponível"
            )

        profile = demographic_distribution(df)

        result = {
            "total_clientes": profile["total_clientes"],
            "genero": profile["por_genero"].to_dict(orient="records"),
            "faixa_etaria": profile["por_faixa_etaria"].to_dict(orient="records"),
            "cidade": profile["por_cidade"].to_dict(orient="records"),
            "estado": profile["por_estado"].to_dict(orient="records"),
            "regiao": profile["por_regiao"].to_dict(orient="records"),
        }

        return result

    except HTTPException:
        raise
    except Exception:
        logger.exception("Erro ao gerar perfil de clientes")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar perfil de clientes"
        )

@router.get(
    "/download",
    summary="Download de relatório",
    description="Gera e salva em disco um relatório consolidado em JSON ou PDF."
)
def download_report(
    format: str = Query(..., description="Formato do relatório: json ou pdf")
):
    repo = SalesRepository(engine)
    df = repo.fetch_dataframe()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Nenhum dado disponível para gerar relatório"
        )

    sales = calculate_sales_metrics(df)
    financial = calculate_financial_metrics(df)
    regional = metrics_by_region(df)

    report = {
        "vendas": sales,
        "financeiro": financial,
        "regional": regional.round(2).to_dict(orient="records"),
    }

    # -------- JSON --------
    if format == "json":
        file_path = REPORTS_DIR / "report.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return FileResponse(
            path=file_path,
            media_type="application/json",
            filename="report.json"
        )

    # -------- PDF --------
    if format == "pdf":
        file_path = REPORTS_DIR / "report.pdf"

        doc = SimpleDocTemplate(str(file_path), pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(
            Paragraph("Relatório Analítico - Hanami API", styles["Title"])
        )

        # ----- TABELA -----
        table_data = [
            ["Região", "Receita Total", "Unidades Vendidas", "Ticket Médio"]
        ]

        for _, row in regional.iterrows():
            table_data.append([
                row["regiao"],
                f"{row['receita_total']:.2f}",
                int(row["unidades_vendidas"]),
                f"{row['ticket_medio']:.2f}",
            ])

        elements.append(Table(table_data))

        # ----- GRÁFICO -----
        plt.figure()
        plt.bar(regional["regiao"], regional["receita_total"])
        plt.title("Receita por Região")
        plt.tight_layout()

        chart_path = REPORTS_DIR / "receita_por_regiao.png"
        plt.savefig(chart_path)
        plt.close()

        elements.append(
            Image(str(chart_path), width=400, height=250)
        )

        doc.build(elements)

        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename="report.pdf"
        )

    # -------- ERRO --------
    raise HTTPException(
        status_code=400,
        detail="Formato inválido. Use json ou pdf."
    )
