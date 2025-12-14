from hanami.services.analytics import (
    calculate_financial_metrics,
    calculate_sales_metrics,
)
from hanami.services.ingestion import load_and_validate_file

# Carrega dados limpos
df = load_and_validate_file("data/raw/vendas_ficticias_10000_linhas.csv")

financial = calculate_financial_metrics(df)
sales = calculate_sales_metrics(df)

print("Financeiro:")
print(financial)

print("\nMétricas de Vendas:")
print(sales)
