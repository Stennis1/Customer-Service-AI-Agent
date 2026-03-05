# Customer Service AI Agent

LangChain-based customer support agent with:
- Retrieval-augmented responses from a local knowledge base (`knowledge/*.txt`, optional PDFs)
- Optional backend API tooling for order/customer workflows
- Two local interfaces: CLI and Streamlit web chat

Repository: `https://github.com/Stennis1/Customer-Service-AI-Agent`
Live URL: `https://customer-service-ai-agent-a97r.onrender.com/`

## Features

- Tool-enabled agent (`search_knowledge_base`, `check_order_status`, `escalate_to_human`)
- Conversation memory (last 10 exchanges)
- Chroma vector store for semantic document retrieval
- Optional REST API integration for live order status/tickets/customers
- CLI mode for terminal usage
- Web mode for browser chat via Streamlit

## Tech Stack

- Python 3.10+
- LangChain
- OpenAI API
- ChromaDB
- Streamlit
- Requests

## Project Structure

```text
.
├── agent.py              # Core agent class and tools wiring
├── app.py                # CLI entrypoint
├── web_app.py            # Streamlit web UI entrypoint
├── knowledge_base.py     # Document loading + vector retrieval
├── api_tools.py          # Optional external API client tools
├── knowledge/            # Support knowledge corpus (.txt/.pdf)
├── requirements.txt      # Top-level dependencies
├── .env.example          # Environment variable template
└── test_setup.py         # Basic OpenAI connection check
```

## Architecture

1. User sends a question in CLI or Web UI.
2. `CustomerServiceAgent` in `agent.py` receives the message.
3. Agent selects tools when needed:
   - `search_knowledge_base` -> semantic search via Chroma in `knowledge_base.py`
   - `check_order_status` -> external API (`api_tools.py`) if configured, else mock fallback
   - `escalate_to_human` -> escalation response
4. Agent returns final answer to the interface.

## Prerequisites

- Python 3.10 or newer
- OpenAI API key
- `pip` and virtual environment support

## Setup

1. Clone and enter project:
```bash
git clone https://github.com/Stennis1/Customer-Service-AI-Agent.git
cd Customer-Service-AI-Agent
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```

5. Edit `.env` with at least:
```env
OPENAI_API_KEY=your_openai_key
```

Optional API integration:
```env
CUSTOMER_API_BASE_URL=https://api.example.com
CUSTOMER_API_KEY=your_customer_api_key
```

## Running Locally

### CLI

```bash
python app.py
```

### Web Interface (Streamlit)

```bash
streamlit run web_app.py
```

Streamlit will print a local URL (typically `http://localhost:8501`).

## Deployment (Render)

This repository includes a Render Blueprint file:
- `render.yaml` in the project root

Live deployment:
- https://customer-service-ai-agent-a97r.onrender.com/

Deploy steps:
1. Push latest code to GitHub.
2. In Render, choose `New` -> `Blueprint`.
3. Select this repository (Render reads `render.yaml` automatically).
4. Set required environment variables in Render:
   - `OPENAI_API_KEY` (required)
   - `OPENAI_MODEL` (optional)
   - `CUSTOMER_API_BASE_URL` and `CUSTOMER_API_KEY` (optional, for live backend API calls)

## Knowledge Base

- Add/update support content under `knowledge/`.
- Supported loaders:
  - `.txt` via `TextLoader`
  - `.pdf` via `PyPDFLoader`
- Chunks are embedded and stored in `./chromadb`.

## Verification

Basic OpenAI connection test:
```bash
python test_setup.py
```

Syntax check:
```bash
python -m py_compile agent.py app.py web_app.py api_tools.py knowledge_base.py
```

## API Tooling Behavior

If `CUSTOMER_API_BASE_URL` and `CUSTOMER_API_KEY` are set:
- `check_order_status` uses live HTTP calls.

If they are not set:
- Agent falls back to mock order-status behavior for `ORD*` IDs.

## Environment Variables

Required:
- `OPENAI_API_KEY`: OpenAI API key used by model and embeddings

Optional:
- `OPENAI_MODEL`: Chat model identifier (default: `openai:gpt-4o-mini`)
- `CUSTOMER_API_BASE_URL`: Base URL for customer/order/support backend
- `CUSTOMER_API_KEY`: Bearer token for backend API
- `LANGCHAIN_API_KEY`: For LangSmith tracing (if you enable it)
- `VECTOR_DB_URL`: Reserved placeholder, not currently used in runtime

## Common Issues

- `OPENAI_API_KEY` missing:
  - Symptom: agent initialization/search errors.
  - Fix: set key in `.env`.

- Empty knowledge results:
  - Symptom: poor/no retrieval output.
  - Fix: ensure docs exist under `knowledge/` and restart app.

- API requests fail:
  - Symptom: order/customer/ticket tool errors.
  - Fix: verify `CUSTOMER_API_BASE_URL`, `CUSTOMER_API_KEY`, backend reachability.

## Development Notes

- Keep `app.py` and `web_app.py` as thin entrypoints; put logic in `agent.py`.
- `knowledge_base.py` provides a backward-compatible alias `KnowledegeBase` for legacy typoed imports.
- Prefer adding tests before expanding tools/agent prompt complexity.

## Next Improvements

- Add `pytest` tests for:
  - Tool behavior
  - Fallback paths when env vars are missing
  - Knowledge retrieval quality
- Add structured logging and request tracing
- Add Dockerfile and compose profile for reproducible local runtime
- Add CI workflow (lint + test + type checks)

## License

No license file is currently included. Add `LICENSE` before public reuse/distribution.
