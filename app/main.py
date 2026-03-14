from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from app.rag import retrieve, index_knowledge_base
from app.llm import ask
from app.prompts import build_prompt

app = FastAPI()

@app.on_event("startup")
def startup():
    index_knowledge_base()

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask_question(query: Query):
    chunks = retrieve(query.text)
    system_prompt = build_prompt(chunks, date.today().isoformat())
    answer = ask(system_prompt, query.text)
    return {"answer": answer, "chunks_used": chunks}

@app.get("/reload")
def reload_knowledge_base():
    index_knowledge_base()
    return {"status": "Knowledge base reloaded"}