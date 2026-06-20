import os
import httpx
import json

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # default local dev

MODEL_NAME = "deepseek-coder"


async def review_code_with_llm(code: str, language: str) -> dict:
    system_instructions = (
        "You are a senior code reviewer. Given a code snippet, you must:\n"
        "1) Explain clearly what the code does.\n"
        "2) Identify potential bugs, edge cases, and security issues.\n"
        "3) Suggest performance, readability, and best-practice improvements.\n"
        "Respond ONLY as a JSON object with keys: logic, bugs, optimizations."
    )

    user_prompt = f"""
{system_instructions}

Language: {language}

Code:
```{language}
{code}
```

Return JSON exactly in this format:
{{
  "logic": "...",
  "bugs": "...",
  "optimizations": "..."
}}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": user_prompt,
        "stream": False,
        "format": "json",
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        resp.raise_for_status()
        data = resp.json()

    content = data.get("response", "{}")
    parsed = json.loads(content)

    return {
        "logic": parsed.get("logic", ""),
        "bugs": parsed.get("bugs", ""),
        "optimizations": parsed.get("optimizations", ""),
    }