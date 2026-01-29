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

    def search(self, filters: dict, limit: int = 100):
        base_query = "SELECT * FROM sales WHERE 1=1"
        params = {}

        if "estado" in filters:
            base_query += " AND estado_cliente = :estado"
            params["estado"] = filters["estado"]

        if "cidade" in filters:
            base_query += " AND cidade_cliente = :cidade"
            params["cidade"] = filters["cidade"]

        if "produto" in filters:
            base_query += " AND nome_produto LIKE :produto"
            params["produto"] = f"%{filters['produto']}%"

        if "categoria" in filters:
            base_query += " AND categoria = :categoria"
            params["categoria"] = filters["categoria"]

        if "start_date" in filters:
            base_query += " AND data_venda >= :start_date"
            params["start_date"] = filters["start_date"]

        if "end_date" in filters:
            base_query += " AND data_venda <= :end_date"
            params["end_date"] = filters["end_date"]

        if "min_valor" in filters:
            base_query += " AND valor_final >= :min_valor"
            params["min_valor"] = filters["min_valor"]

        if "max_valor" in filters:
            base_query += " AND valor_final <= :max_valor"
            params["max_valor"] = filters["max_valor"]

        base_query += " ORDER BY data_venda DESC LIMIT :limit"
        params["limit"] = limit

        with self.engine.connect() as conn:
            return conn.execute(text(base_query), params).mappings().all()