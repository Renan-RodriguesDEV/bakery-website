import json
import os
from typing import Dict

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from src.chatbot.tools import find_all_products

load_dotenv()
API_KEY = (
    os.getenv("GOOGLE_API_KEY")
    if os.getenv("GOOGLE_API_KEY")
    else st.secrets["GOOGLE_API_KEY"]
)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, api_key=API_KEY)


PROMPT = """
Você é um assistente da padaria "Padaria da Vila".
RETORNE SOMENTE UM JSON VÁLIDO (UTF-8) SEM markdown, SEM explicações, SEM cercas de código.
Campos obrigatórios:
{
  "font": ["Fonte ou origem sucinta da resposta (máx 2 itens)"],
  "message": "Resposta objetiva em português sobre panificação/padaria. Use **negrito** apenas quando realmente necessário."
}
REGRAS:
- Não inclua crases ou tres crases nem linguagem.
- Não inclua texto antes ou depois do JSON.
- Se a pergunta não for sobre padaria, ou sobre este sistema de padaria interno, responda com:
  {"font": ["interno"], "message": "Posso auxiliar apenas em assuntos da padaria e panificação."}
"""


class Response(BaseModel):
    font: list[str] = Field(title="font:", max_length=100)
    message: str = Field(title="message:", max_length=500)


tools = [find_all_products]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
)


def ask_chat(answer) -> Dict:
    response = agent.invoke(
        {"input": f"{PROMPT}\n\nPergunta: {answer}", "chat_history": []}
    )
    print(response)
    print(type(response.get("output")))
    try:
        if isinstance(response.get("output"), str):
            return json.loads(response.get("output"))
        return response.get("output")
    except json.JSONDecodeError:
        return {"font": ["interno"], "message": "Erro ao processar a resposta."}
