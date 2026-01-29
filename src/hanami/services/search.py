from datetime import date

def build_search_filters(
    estado: str | None,
    cidade: str | None,
    produto: str | None,
    categoria: str | None,
    start_date: date | None,
    end_date: date | None,
    min_valor: float | None,
    max_valor: float | None,
):
    filters = {}

    if estado:
        filters["estado"] = estado

    if cidade:
        filters["cidade"] = cidade

    if produto:
        filters["produto"] = produto

    if categoria:
        filters["categoria"] = categoria

    if start_date:
        filters["start_date"] = start_date

    if end_date:
        filters["end_date"] = end_date

    if min_valor is not None:
        filters["min_valor"] = min_valor

    if max_valor is not None:
        filters["max_valor"] = max_valor

    return filters
