from hanami.services.ingestion import load_and_validate_file

df = load_and_validate_file("data/raw/vendas_ficticias_10000_linhas.csv")
print(df.head())
print(df.dtypes)
