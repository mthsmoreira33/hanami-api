from pathlib import Path
import pandas as pd


class InvalidDataError(ValueError):
    """Erro levantado quando o arquivo não atende ao contrato esperado."""
    pass


REQUIRED_COLUMNS = {
    "id_transacao",
    "data_venda",
    "valor_final",
    "subtotal",
    "desconto_percent",
    "canal_venda",
    "forma_pagamento",
    "cliente_id",
    "idade_cliente",
}

OPTIONAL_COLUMNS = {
    "status_entrega",
    "regiao",
}

VALID_SALES_CHANNELS = {
    "online",
    "loja física",
    "marketplace",
    "telefone",
    "app mobile",
}

VALID_PAYMENT_METHODS = {
    "cartão crédito",
    "cartão débito",
    "pix",
    "boleto",
}


def load_and_validate_file(file_path: str | Path) -> pd.DataFrame:
    """
    Lê arquivos CSV ou XLSX, valida estrutura, tipos e regras semânticas,
    retornando um DataFrame Pandas confiável.
    """

    file_path = Path(file_path)

    # Leitura do arquivo conforme extensão
    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(file_path)
    else:
        raise InvalidDataError(
            f"Formato de arquivo não suportado: {file_path.suffix}"
        )

    # Validação de colunas obrigatórias
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise InvalidDataError(
            f"Colunas obrigatórias ausentes: {', '.join(sorted(missing_columns))}"
        )

    # Conversão de colunas numéricas
    numeric_columns = [
        "valor_final",
        "subtotal",
        "desconto_percent",
        "idade_cliente",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Conversão de datas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")

    # Padronização de texto
    df["canal_venda"] = (
        df["canal_venda"].astype(str).str.strip().str.lower()
    )
    df["forma_pagamento"] = (
        df["forma_pagamento"].astype(str).str.strip().str.lower()
    )

    # Validações semânticas
    semantic_errors: list[str] = []

    invalid_sales_channel = ~df["canal_venda"].isin(VALID_SALES_CHANNELS)
    if invalid_sales_channel.any():
        semantic_errors.append("valores inválidos em canal_venda")

    invalid_payment_method = ~df["forma_pagamento"].isin(VALID_PAYMENT_METHODS)
    if invalid_payment_method.any():
        semantic_errors.append("valores inválidos em forma_pagamento")

    invalid_discount = (
        (df["desconto_percent"] < 0) | (df["desconto_percent"] > 100)
    )
    if invalid_discount.any():
        semantic_errors.append("desconto_percent fora do intervalo 0–100")

    invalid_final_value = df["valor_final"] > df["subtotal"]
    if invalid_final_value.any():
        semantic_errors.append("valor_final maior que subtotal")

    if semantic_errors:
        raise InvalidDataError(
            "Falhas de validação semântica: " + "; ".join(semantic_errors)
        )

    # Remoção controlada de linhas críticas nulas
    total_rows_before = len(df)
    df = df.dropna(subset=["valor_final", "data_venda"])
    removed_rows = total_rows_before - len(df)

    if removed_rows > 0:
        if removed_rows / total_rows_before > 0.05:
            raise InvalidDataError(
                f"{removed_rows} linhas removidas por dados críticos nulos "
                f"({removed_rows / total_rows_before:.1%} do total)"
            )

    return df
