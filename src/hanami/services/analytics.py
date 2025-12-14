import pandas as pd


def calculate_financial_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas financeiras básicas.

    Retorna:
        net_revenue: soma do valor final das vendas
        gross_profit: soma do lucro bruto (se custo_produto existir)
    """
    net_revenue = df["valor_final"].sum()

    if "custo_produto" in df.columns:
        gross_profit = (df["valor_final"] - df["custo_produto"]).sum()
    else:
        gross_profit = None

    return {
        "net_revenue": float(net_revenue),
        "gross_profit": float(gross_profit) if gross_profit is not None else None,
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
        "total_sales": float(total_sales),
        "transaction_count": int(transaction_count),
        "average_per_transaction": float(average_per_transaction),
    }
