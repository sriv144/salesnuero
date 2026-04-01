# SalesNeuro 🧠

> **AI-powered buyer psychology intelligence and personalized sales outreach platform.**

SalesNeuro uses a multi-agent AI pipeline to research prospects, build psychological profiles (Big Five / DISC), and generate hyper-personalized cold email sequences — all in one automated workflow.

---

## ✨ Features

- 🔍 **Prospect Research** — Automated OSINT via Tavily web search
- 🧬 **Psychological Profiling** — Big Five (OCEAN) scoring + DISC type classification
- 🎯 **Sales Strategy** — AI-ranked value propositions matched to buyer psychology
- ✉️ **Email Copywriting** — 3-email cold outreach sequences tailored per prospect
- ⚡ **RAG-Augmented** — ChromaDB vector store for personality & product knowledge
- 🖥️ **Full-Stack** — Next.js frontend + FastAPI backend

---

## 🏗️ Architecture

```
salesneuro/
├── backend/                  # FastAPI + CrewAI pipeline
│   ├── app/
│   │   ├── agents/           # CrewAI crew (4-agent pipeline)
│   │   ├── api/              # REST endpoints
│   │   ├── core/             # Config & settings
│   │   ├── models/           # Pydantic schemas
│   │   ├── rag/              # ChromaDB retrieval
│   │   └── services/         # Business logic
│   ├── ingest_rag.py         # Populate the vector store
│   └── requirements.txt
├── frontend/                 # Next.js 15 app
│   └── src/
│       ├── app/              # App Router pages
│       ├── components/       # UI components
│       └── lib/              # API client
└── data/
    └── chroma_db/            # Vector store (auto-generated, gitignored)
```

### Agent Pipeline

```
Input: Prospect Name + Company
        │
        ▼
┌─────────────────────┐
│  1. Researcher      │  ← Tavily web search
│  Lead Prospect      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Profiler        │  ← ChromaDB personality corpus
│  Psych Profiler     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Strategist      │  ← ChromaDB product corpus
│  Sales Strategist   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Copywriter      │  ← 3-email outreach sequence
│  Outreach Writer    │
└─────────────────────┘
        │
        ▼
Output: Research + Profile + Strategy + Emails
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [NVIDIA NIM API key](https://build.nvidia.com/) (free tier available)
- [Tavily API key](https://tavily.com/) (free tier: 1,000 searches/month)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/salesneuro.git
cd salesneuro
```

### 2. Backend setup

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate        # Windows
# source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Configure `.env`

```env
NVIDIA_API_KEY="nvapi-..."
TAVILY_API_KEY="tvly-..."
```

### 4. Ingest RAG data (first time only)

```bash
python ingest_rag.py
```

### 5. Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend runs at → `http://localhost:8000`  
API docs (Swagger) → `http://localhost:8000/docs`

### 6. Frontend setup

```bash
cd ../frontend
npm install
npm run dev
```

Frontend runs at → `http://localhost:3000`

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/run` | Run the full 4-agent pipeline |
| `GET` | `/api/prospects` | List saved prospect results |

### Example Request

```bash
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"prospect_name": "Elon Musk", "company_name": "Tesla"}'
```

---

## 🤖 Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Meta Llama 3.1 70B via NVIDIA NIM |
| Agent Framework | CrewAI |
| Vector Store | ChromaDB |
| Embeddings | `all-MiniLM-L6-v2` (SentenceTransformers) |
| Web Search | Tavily API |
| Backend | FastAPI + Uvicorn |
| Frontend | Next.js 15 (App Router) |
| Validation | Pydantic v2 |

---

## 📁 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NVIDIA_API_KEY` | ✅ | NVIDIA NIM API key for Llama 3.1 70B |
| `TAVILY_API_KEY` | ✅ | Tavily search API key |

Never commit your `.env` file. A `.env.example` template is provided.

---

## 🛡️ Security Notes

- `.env` is gitignored — **never commit real API keys**
- `data/chroma_db/` is gitignored — regenerate locally with `ingest_rag.py`
- `venv/` and `node_modules/` are excluded from the repo

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">Built with CrewAI · FastAPI · Next.js</p>
