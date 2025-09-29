from typing import Any

from langchain.tools import tool
from sqlalchemy import text
from src.models.entities.connection_handler import get_db_session


@tool
def find_all_products(typed: str = "listar") -> list[dict[str, Any]] | list:
    """Find all products in the bakery."""
    with get_db_session() as session:
        query = session.execute(
            text("SELECT nome,preco,estoque,categoria FROM produtos")
        )
        results = query.fetchall()
        if results:
            return [r._asdict() for r in results]
    return []
