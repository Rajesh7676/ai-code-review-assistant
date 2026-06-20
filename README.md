# AI Code Review Assistant

An **AI-powered code review tool** that explains your code, highlights potential bugs, and suggests optimizations using a local LLM (Ollama + DeepSeek Coder) behind a FastAPI backend and a Streamlit frontend.

## Features

- Paste any code snippet and select the language.
- Get a high-level explanation of what the code is doing.
- See potential bugs, edge cases, and risky patterns.
- Receive suggestions for optimizations, readability, and best practices.
- Run everything locally using Docker and a self-hosted LLM (no external API required).

## Tech stack

- LLM: Ollama with the `deepseek-coder` model  
- Backend: FastAPI, HTTPX  
- Frontend: Streamlit, Requests  
- Containerization: Docker, Docker Compose  
- Language: Python 3.11  

## Architecture

- Ollama  
  - Runs the DeepSeek Coder model.  
  - Exposes the LLM API at `http://ollama:11434/api/generate`.

- Backend (FastAPI)  
  - Exposes a `/review` endpoint.  
  - Accepts code and language as input.  
  - Builds a prompt and calls the Ollama API.  
  - Returns structured JSON with `logic`, `bugs`, and `optimizations`.

- Frontend (Streamlit)  
  - Simple UI to paste code and choose language.  
  - Sends a request to the backend.  
  - Renders the explanation, bug list, and suggestions.

## Getting started with Docker

Prerequisites:

- Docker Desktop installed and running.

Clone the repository and start the stack:

```bash
git clone https://github.com/Rajesh7676/ai-code-review-assistant.git
cd ai-code-review-assistant
docker compose up --build
```

Pull the model inside the Ollama container:

```bash
docker exec -it ollama ollama pull deepseek-coder
```

Then open:

- Streamlit UI: `http://localhost:8501`  
- FastAPI docs: `http://localhost:8000/docs`  

## Running locally without Docker

1. Start Ollama and pull the model:

```bash
ollama serve
ollama pull deepseek-coder
```

2. Start the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

3. Start the frontend:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in the browser and use the app.

## Example

Input:

```python
def divide(a, b):
    return a / b
```

The assistant might:

- Explain that this function divides `a` by `b`.  
- Point out a possible division-by-zero error.  
- Suggest adding error handling and type hints.

## Future improvements

- Add severity levels for issues (high, medium, low).
- Support more languages with dedicated prompts.
- Keep a history of past reviews per user.
- Stream partial responses for a faster experience.
