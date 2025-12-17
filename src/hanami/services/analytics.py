import pandas as pd


def calculate_financial_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas financeiras básicas.

    Retorna:
        receita_liquida: soma do valor final das vendas
        lucro_bruto: soma do lucro bruto (se custo_produto existir)
    """
    net_revenue = df["valor_final"].sum()

    if "custo_produto" in df.columns:
        gross_profit = (df["valor_final"] - df["custo_produto"]).sum()
    else:
        gross_profit = None

    return {
        "receita_liquida": float(net_revenue),
        "lucro_bruto": float(gross_profit) if gross_profit is not None else None,
    }


def calculate_sales_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas agregadas de vendas.
    """
    total_sales = df["valor_final"].sum()
    transaction_count = len(df)

    average_per_transaction = (
        total_sales / transaction_count
        if transaction_count > 0
        else 0.0
    )

    return {
        "total_vendas": float(total_sales),
        "numero_transacoes": int(transaction_count),
        "media_por_transacao": float(average_per_transaction),
    }

def calculate_product_analysis(df: pd.DataFrame) -> list[dict]:
    """
    Gera análise agregada por produto.

    Retorna uma lista de dicionários com:
        nome_produto
        quantidade_vendida
        total_arrecadado
    """

    required_columns = {"nome_produto", "quantidade", "valor_final"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Colunas necessárias para análise de produto ausentes: {', '.join(missing)}"
        )

    grouped_df = (
        df
        .groupby("nome_produto", as_index=False)
        .agg(
            sold_quantity=("quantidade", "sum"),
            total_revenue=("valor_final", "sum"),
        )
    )

    grouped_df = grouped_df.rename(
        columns={
            "sold_quantity": "quantidade_vendida",
            "total_revenue": "total_arrecadado",
        }
    )

    return grouped_df.to_dict(orient="records")