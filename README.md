# 🧠 MCP Server (Model Context Protocol)

The **MCP Server** is a lightweight microservice that connects real-world information (like web search results) to language models (LLMs) to improve prompt understanding and response generation. This pattern enables you to dynamically provide *context* to LLMs before asking them a question.

## 📌 What is MCP?

**MCP (Model Context Protocol)** is a **design pattern**, not a library. It describes how to build applications that:

1. **Receive a user prompt**
2. **Enrich the prompt with context** (from web search, databases, documents, etc.)
3. **Send the enriched prompt to an LLM** (like OpenAI, Claude, or vLLM)
4. **Return the LLM's response**

This project implements MCP as a **FastAPI server**.

---

## ⚙️ What This MCP Server Does

This particular server:

* Accepts prompts at a REST endpoint (`/generate`)
* Uses [LinkUp](https://linkup.ai) to do web search and fetch real-time information
* Sends enriched prompt + context to a local [vLLM](https://github.com/vllm-project/vllm) model server
* Returns the model’s generated response

---

## 🗂️ Folder Structure

```
.
├── mcp_server.py     # Main MCP server implementation
├── test_client.py    # (Optional) Simple test client to interact with your MCP server
├── requirements.txt  # Python dependencies
├── .env              # API keys and secrets
```

---

## 🥪 Example Usage

Send a POST request to your MCP server:

```bash
curl -X POST http://localhost:8091/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the future of quantum computing?"}'
```

Response:

```json
{
  "response": "Quantum computing is expected to..."
}
```

---

## 📥 Prerequisites

Make sure your environment has:

* Python 3.10+
* Access to `vLLM` (running on `localhost:8000`)
* A working [LinkUp API key](https://linkup.ai)

---

## 🔧 Installation & Setup

### 1. Clone This Repo

```bash
git clone https://github.com/your-org/mcp-server.git
cd mcp-server
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Set Up `.env` File

Create a `.env` file with your LinkUp API key:

```env
LINKUP_API_KEY=your-linkup-api-key-here
```

---

## 🚀 Run the MCP Server

```bash
python mcp_server.py
```

Should show something like:

```
INFO:     Uvicorn running on http://0.0.0.0:8091
```

---

## 🧠 How the Code Works

```python
# 1. Accept prompt
@app.post("/generate")
def generate_response(request: PromptRequest):
    prompt = request.prompt

    # 2. Get real-time web context from LinkUp
    search_results = perform_web_search(prompt)

    # 3. Combine context with user prompt
    full_prompt = f"{search_results}\n\nUser Prompt: {prompt}"

    # 4. Call vLLM for response
    model_output = call_vllm(full_prompt)

    return {"response": model_output}
```

---

## 👤 Streamlit UI (Optional)

Run this for a simple web interface:

```bash
streamlit run app.py --server.address 0.0.0.0
```

If you're on a cloud container (like AI Stack), forward the port to view in a browser:

```bash
kubectl port-forward pod/<your-pod-name> 8501:8501
```

---

## 🧩 What's Next?

You can customize this server to:

* Use other context sources (e.g., PDF, vector DB)
* Switch models (OpenAI, Claude, Gemini)
* Handle multi-turn conversations

---

## 📚 Credits

* [vLLM](https://github.com/vllm-project/vllm)
* [LinkUp](https://linkup.ai)
* [FastAPI](https://fastapi.tiangolo.com)

---

## 🧠 Summary

This MCP server gives your LLM the **eyes and ears** it needs by pulling in real-world info — making your AI smarter, more accurate, and more up-to-date.
