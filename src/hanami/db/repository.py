import pandas as pd
from sqlalchemy.engine import Engine


class SalesRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def save_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str = "vendas",
    ) -> int:
        df.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False
        )
        return len(df)
