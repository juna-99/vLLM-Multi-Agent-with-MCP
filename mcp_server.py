from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Get LinkUp API key from environment or hardcode here
LINKUP_API_KEY = os.getenv("LINKUP_API_KEY") 

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_response(request: PromptRequest):
    prompt = request.prompt

    # 1. Web search via LinkUp
    search_results = linkup_search(prompt)

    # 2. Generate response via vLLM (pass context from web)
    model_response = get_model_response(prompt, search_results)

    return {"response": model_response}


def linkup_search(query: str) -> str:
    """Search using LinkUp via REST API"""
    try:
        url = "https://api.linkup.ai/search"
        headers = {
            "Authorization": f"Bearer {LINKUP_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "depth": "deep",
            "output_type": "searchResults"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result_data = response.json()
        return result_data.get("results", "No search results.")
    except Exception as e:
        return f"LinkUp Error: {str(e)}"


def get_model_response(prompt: str, search_results: str) -> str:
    """Send combined context + prompt to vLLM"""
    full_prompt = f"Context from web:\n{search_results}\n\nQuestion: {prompt}"
    try:
        url = "http://localhost:8000/v1/chat/completions"
        payload = {
            "model": "Qwen/Qwen2.5-1.5B-Instruct",
            "messages": [
                {"role": "user", "content": full_prompt}
            ]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Model Error: {str(e)}"

# Run the MCP server with: python mcp_server.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
