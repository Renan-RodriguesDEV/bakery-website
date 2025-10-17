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


@tool(
    "get_data_FAQ",
    description="Retorna perguntas frequentes (localização, horários, contato, pagamentos). Use para perguntas sobre localização/horário/contato.",
)
def get_data_FAQ(query: str = "Perguntas Frequentes") -> str:
    """Get FAQ data as a string."""
    return """
1. Onde fica localizada a padaria?
R: A padaria está localizada na Rua Pedro Gonsalves da Silva, nº 11, Vila cap. Cesario

2. Quais são os horários de funcionamento?
R: A padaria funciona nos dias de semana, das 7h às 19h. E nos finais de semana, das 8h às 18h. O horário de funcionamento pode variar em feriados.

3. Quais métodos de pagamento são aceitos?
R: Aceitamos dinheiro, cartões de crédito e débito, além de pagamentos via Pix.

4. A padaria aceita encomendas para eventos?
R: Sim, aceitamos encomendas para aniversários, casamentos e outros eventos. Recomenda-se fazer a encomenda com antecedência.

5. Quais são os meios de contato da padaria?
R: Você pode entrar em contato conosco pelo telefone e/ou whatsapp nos números: (14) 99752-6985 e/ou (19) 99872-2472. Ou pelo e-mail jeffersonrodrigues7110@gmail.com.

6. Vocês fazem entregas?
R: Sim, fazemos entregas na região próxima à padaria. Consulte as condições e taxas de entrega no momento do pedido. Para realizar pedidos via WhatsApp, utilize o número (14) 99752-6985 ou (19) 99872-2472. Para pedidos na plataforma, acesse nosso site, faça seu pedido e escolha a opção de "retirada" em "meus pedidos".
"""
