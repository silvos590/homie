# Homie #

Simple home-assistant

## Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

### Pull the model — Q4_K_M is the sweet spot: good quality, ~4.8GB, fits comfortably in 8GB RAM
ollama pull llama3.1:8b-instruct-q4_K_M

### Test it
ollama run llama3.1:8b-instruct-q4_K_M "Say hello"

### Also pull embedding model
ollama pull nomic-embed-text

## How to run
### Terminal 1 — Ollama (or set as systemd service)
ollama serve

### Terminal 2 — FastAPI
cd home-assistant
uvicorn app.main:app --host 0.0.0.0 --port 8000

### Terminal 3 — Telegram bot - WIP
python -m app.bot