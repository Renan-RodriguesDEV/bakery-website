import os
from typing import Dict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, api_key=API_KEY)


PROMPT = """
Você é uma assistente android da padaria "Padaria da Vila". Responda apenas com um JSON válido
no formato JSON/Dict do python com chaves e valores:
{
  "font": ["fonte1 (url ou referência)", "fonte2"],
  "message": "Resposta em markdown, objetiva e baseada apenas em dados da padaria e panificação."
}
"""


class Response(BaseModel):
    font: list[str] = Field(title="font:", max_length=100)
    message: str = Field(title="message:", max_length=300)


llm.with_structured_output(Response)


def ask_chat(answer) -> Dict:
    response = llm.invoke([SystemMessage(content=PROMPT), HumanMessage(content=answer)])
    return response
