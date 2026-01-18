from pydantic import BaseModel, RootModel, ConfigDict
from typing import List, Dict, Any


class SalesSummaryResponse(BaseModel):
    total_vendas: float
    numero_transacoes: int
    media_por_transacao: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_vendas": 250000.0,
                "numero_transacoes": 1240,
                "media_por_transacao": 201.61
            }
        }
    )


class ProductAnalysisItem(BaseModel):
    nome_produto: str
    quantidade_vendida: int
    total_arrecadado: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome_produto": "Notebook",
                "quantidade_vendida": 120,
                "total_arrecadado": 360000.0
            }
        }
    )


class FinancialMetricsResponse(BaseModel):
    receita_liquida: float
    lucro_bruto: float | None
    custo_total: float | None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "receita_liquida": 125000.5,
                "lucro_bruto": 42000.75,
                "custo_total": 83000.0
            }
        }
    )


class RegionalPerformanceResponse(
    RootModel[Dict[str, Dict[str, float]]]
):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Sudeste": {
                    "receita_total": 100000.0,
                    "unidades_vendidas": 350,
                    "numero_transacoes": 200,
                    "custo_total": 60000.0,
                    "lucro_total": 40000.0,
                    "ticket_medio": 500.0
                }
            }
        }
    )


class CustomerProfileResponse(BaseModel):
    total_clientes: int
    genero: List[Dict[str, Any]]
    faixa_etaria: List[Dict[str, Any]]
    cidade: List[Dict[str, Any]]
    estado: List[Dict[str, Any]]
    regiao: List[Dict[str, Any]]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_clientes": 300,
                "genero": [
                    {"valor": "M", "contagem": 180, "percentual": 60.0},
                    {"valor": "F", "contagem": 120, "percentual": 40.0}
                ]
            }
        }
    )
