import pandas as pd
from typing import Optional

_DATAFRAME_CACHE: Optional[pd.DataFrame] = None


def store_dataframe(df: pd.DataFrame) -> None:
    global _DATAFRAME_CACHE
    _DATAFRAME_CACHE = df


def get_dataframe() -> pd.DataFrame:
    if _DATAFRAME_CACHE is None:
        raise RuntimeError("Nenhum dataset carregado")
    return _DATAFRAME_CACHE
