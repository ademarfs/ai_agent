from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from vector import md_rag
import os

app = FastAPI()

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2Templates
templates = Jinja2Templates(directory="templates")

ollama_url = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
model = OllamaLLM(model="llama3.2", base_url=ollama_url)

template = """
Você é um especialista em responder perguntas sobre assuntos jurídicos.

Você é um excelente juiz e vai responder as perguntas com base no que foi informado no documento.

Here are some relevant documents: {documents}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

md_files = "./markdown_files"
retriever = md_rag(source_directory=md_files, db_path="chroma_md_db", collection_name="tech_files")
print("Retriever ready.")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(question: dict):
    user_question = question.get("question")
    if not user_question:
        return {"response": "Por favor, forneça uma pergunta."}
    
    docs = retriever.invoke(user_question)
    result = chain.invoke({"documents": docs, "question": user_question})
    return {"response": result}