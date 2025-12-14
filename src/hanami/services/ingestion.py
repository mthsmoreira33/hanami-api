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

VALID_CANAL_VENDA = {
    "online",
    "loja física",
    "marketplace",
    "telefone",
    "app mobile",
}

VALID_FORMA_PAGAMENTO = {
    "cartão crédito",
    "cartão débito",
    "pix",
    "boleto",
}


def load_and_validate_file(file_path: str | Path) -> pd.DataFrame:
    """
    Lê arquivos CSV ou XLSX, valida, padroniza e valida semanticamente
    os dados, retornando um DataFrame Pandas confiável.
    """

    file_path = Path(file_path)

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(file_path)
    else:
        raise InvalidDataError(
            f"Formato de arquivo não suportado: {file_path.suffix}"
        )

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise InvalidDataError(
            f"Colunas obrigatórias ausentes: {', '.join(sorted(missing_columns))}"
        )

    numeric_columns = [
        "valor_final",
        "subtotal",
        "desconto_percent",
        "idade_cliente",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")

    df["canal_venda"] = (
        df["canal_venda"].astype(str).str.strip().str.lower()
    )
    df["forma_pagamento"] = (
        df["forma_pagamento"].astype(str).str.strip().str.lower()
    )

    semantic_errors = []

    invalid_canal = ~df["canal_venda"].isin(VALID_CANAL_VENDA)
    if invalid_canal.any():
        semantic_errors.append("valores inválidos em canal_venda")

    invalid_pagamento = ~df["forma_pagamento"].isin(VALID_FORMA_PAGAMENTO)
    if invalid_pagamento.any():
        semantic_errors.append("valores inválidos em forma_pagamento")

    invalid_desconto = (df["desconto_percent"] < 0) | (df["desconto_percent"] > 100)
    if invalid_desconto.any():
        semantic_errors.append("desconto_percent fora do intervalo 0–100")

    invalid_valor = df["valor_final"] > df["subtotal"]
    if invalid_valor.any():
        semantic_errors.append("valor_final maior que subtotal")

    if semantic_errors:
        raise InvalidDataError(
            "Falhas de validação semântica: " + "; ".join(semantic_errors)
        )

    before_rows = len(df)
    df = df.dropna(subset=["valor_final", "data_venda"])
    removed_rows = before_rows - len(df)

    if removed_rows > 0:
        if removed_rows / before_rows > 0.05:
            raise InvalidDataError(
                f"{removed_rows} linhas removidas por dados críticos nulos "
                f"({removed_rows / before_rows:.1%} do total)"
            )

    return df
