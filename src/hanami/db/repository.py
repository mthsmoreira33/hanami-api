import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


class SalesRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def save_dataframe(self, df: pd.DataFrame) -> int:
        df.to_sql(
            "sales",
            self.engine,
            if_exists="append",
            index=False,
        )
        return len(df)

    def fetch_all(self) -> pd.DataFrame:
        query = text("SELECT * FROM sales")

        with self.engine.connect() as conn:
            df = pd.read_sql(query, conn)

        return df

    def fetch_dataframe(self) -> pd.DataFrame:
        """
        Retorna todas as vendas como DataFrame.
        """
        query = text("SELECT * FROM sales")
        return pd.read_sql(query, self.engine)