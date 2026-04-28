# SalesNeuro

SalesNeuro is an AI-powered B2B buyer-psychology intelligence and personalized outreach platform. It runs a multi-agent CrewAI pipeline that gathers public information on a prospect, builds a Big Five (OCEAN) and DISC psychological profile, and drafts a cold-outreach email tuned to that profile rather than to a generic template.

The stack is split cleanly between a Python FastAPI backend that hosts the agents and a Next.js frontend that drives the workflow.

## Highlights

- **Multi-agent OSINT**: CrewAI orchestrates research agents that pull public signals (Tavily web search) about a target prospect.
- **Psychology profiling**: agents score the prospect on Big Five (OCEAN) and DISC dimensions and surface persuasion levers.
- **Personalized copywriting**: a writer agent drafts a cold email tuned to the resolved profile, not a static template.
- **RAG corpus**: ChromaDB stores role/industry context so agents can ground messaging in domain-specific knowledge.
- **Modern UX**: Next.js + React + Tailwind frontend with a single "run prospect" workflow.
- **Pluggable LLM provider**: LiteLLM under the hood, so the same agents can call Anthropic Claude or any OpenAI-compatible endpoint (NVIDIA NIM, OpenRouter, local).

## Architecture

```
           ┌─────────────────────┐
           │ Next.js frontend     │
           │ (frontend/, app/)   │
           └──────────┬─────────┘
                      │ POST /api/run
                      ▼
           ┌─────────────────────┐
           │ FastAPI backend      │
           │ (backend/app/main)   │
           └──────────┬─────────┘
                      │
         ┌───────────┼───────────────────┐
         ▼                                  ▼
  ┌─────────────────┐             ┌──────────────────┐
  │ CrewAI pipeline   │             │ ChromaDB        │
  │ (crew_pipeline)   │  ──RAG──▶  │ corpus          │
  └───────┬─────────┘             └──────────────────┘
          │
   ┌──────┼───────┐
   ▼            ▼
 ┌─────────┐  ┌────────────┐
 │ Tavily │  │ LiteLLM │  ◄ Anthropic / NIM / OpenAI-compatible
 │ search │  │ client  │
 └─────────┘  └────────────┘
```

## Tech Stack

- **Backend**: FastAPI, Python 3.10+, CrewAI, LiteLLM, ChromaDB, Tavily.
- **Frontend**: Next.js (App Router), React, Tailwind CSS.
- **LLM provider**: any LiteLLM-compatible endpoint. Default `.env.example` is wired for Anthropic Claude.

## Project Structure

```
.
├── backend/
│   ├── app/                  # FastAPI app + route handlers
│   ├── crew_pipeline.py      # CrewAI agent definitions and orchestration
│   ├── ingest_rag.py         # Loads raw_data/ into ChromaDB
│   ├── raw_data/             # Source documents for the RAG corpus
│   ├── requirements.txt
│   ├── .env.example          # Backend env template
│   ├── test_env.py           # Quick env / provider sanity check
│   └── test_gemini.py        # Provider-specific smoke test
├── frontend/                 # Next.js app
├── .env.example              # Top-level template
└── README.md
```

## Prerequisites

- Python **3.10+**
- Node.js **18+** with npm
- An LLM API key (Anthropic Claude recommended; any LiteLLM-compatible provider works)
- A [Tavily](https://tavily.com) API key for web research

## Quick Start

You'll need two terminals: one for the FastAPI backend and one for the Next.js frontend.

### 1. Configure environment variables

Copy the backend template and fill in your keys:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```dotenv
ANTHROPIC_API_KEY="sk-ant-..."
TAVILY_API_KEY="tvly-..."
```

### 2. Run the backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# Build the ChromaDB RAG corpus (run once, or after changing raw_data/)
python ingest_rag.py

# Start the API
uvicorn app.main:app --reload --port 8000
```

The backend is live at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`.

### 3. Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend is live at `http://localhost:3000`.

## API Surface

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Liveness probe |
| `GET` | `/docs` | Swagger UI |
| `POST` | `/api/run` | Execute the full prospecting pipeline for a target |

Use the Swagger UI to inspect request/response shapes and test calls without the frontend.

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | Yes (default) | API key used by LiteLLM when calling Claude. |
| `TAVILY_API_KEY` | Yes | Powers the web research agent. |
| `LITELLM_MODEL` | No | Override the LiteLLM model id (e.g. `anthropic/claude-3-5-sonnet-latest`, `nvidia/...`, `openai/...`). |
| `CHROMA_DB_PATH` | No | Override where ChromaDB persists the RAG corpus. |
| `BACKEND_URL` | No | Used by the frontend to point at a non-default backend host. |

## Adding RAG Content

Drop new source documents into `backend/raw_data/` and re-run the ingestion script:

```bash
cd backend
python ingest_rag.py
```

The script chunks and embeds the documents into ChromaDB so the agents can retrieve them at runtime.

## Roadmap

- Add a Postgres-backed run history so prospect reports persist across restarts.
- Streaming agent traces in the frontend (current run is one-shot).
- Add a CI workflow (lint + frontend build + backend smoke tests).
- Ship a Dockerfile and docker-compose stack for one-command local setup.
- Plug in additional OSINT sources beyond Tavily (LinkedIn-via-public-pages, Crunchbase open data).

## Notes

- The repo's default branch is `master` (not `main`).
- LLM costs are real — the pipeline can issue several calls per prospect run. Start with Haiku/lighter models while iterating.
- Tavily has a generous free tier but rate-limits aggressively; back off if you see 429s.
