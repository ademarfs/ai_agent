Rode esses comandos na ordem:
1. cria um ambiente virtual: "py -m venv .venv" depois entra nele
2. pip install -r requirements.txt
3. pip install ollama pull llama3.2
4. pip install ollama pull mxbai-embed-large
5. uvicorn app:app --reload