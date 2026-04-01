# SalesNeuro

SalesNeuro is an AI-powered B2B Buyer Psychology Intelligence and Personalized Outreach Platform. It uses state-of-the-art language models and multi-agent systems via [CrewAI](https://github.com/joaomdmoura/crewAI) to deeply analyze prospects and draft highly personalized, psychological sales outreach.

## 🚀 Features

- **Automated Open-Source Intelligence:** Agents perform automated web searches and gather public information on targets via Tavily.
- **Psychological Profiling:** Utilizes Big Five (OCEAN) and DISC profile frameworks to match product strengths with human psychology.
- **Dynamic AI Copywriting:** Tailors cold emails based on the resulting psychological profiles rather than generic templates.
- **Modern Stack:** 
  - **Frontend:** Next.js, React, Tailwind CSS.
  - **Backend:** FastAPI, Python, CrewAI, LiteLLM (integrating with NVIDIA NIM / OpenAI compatible platforms), ChromaDB.

## 🛠 Prerequisites

- Node.js (v18+)
- Python (3.10+)

## 💻 Running Locally

You'll need two separate terminal windows to run both the frontend and the backend.

### 1. Setup Environment Variables

In the `backend` directory, create a `.env` file referencing `.env.example`:
```bash
TAVILY_API_KEY="your_tavily_key"
NVIDIA_API_KEY="your_nvidia_nim_key"
```

### 2. Run the Backend

Navigate to the `backend` directory, set up the virtual environment, install dependencies, and run the FastAPI server.

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

# Run an initial RAG ingestion (required for ChromaDB corpus setup)
python ingest_rag.py

# Start the server
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000`

### 3. Run the Frontend

Navigate to the `frontend` directory, install packages, and spin up the development server.

```bash
cd frontend
npm install
npm run dev
```
Frontend will be live at `http://localhost:3000`

## 🧠 Using The API Direct

Head to `http://localhost:8000/docs` to interact directly with the Swagger UI and test the `/api/run` prospect execution endpoint.
