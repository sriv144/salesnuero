# Research Log

A running log of automated improvement runs against this repo.

## 2026-04-28 — Auto-Researcher v4

**Resume score (start of run):** 64 / 100

- Tech stack prestige: 18 (CrewAI multi-agent, LiteLLM, ChromaDB, Next.js)
- Commit recency: 17 (pushed 2026-04-14)
- Feature completeness: 14 (full FE+BE, but coverage is thin)
- Stars / visibility: 7
- README quality: 8 (decent intro but missing architecture, API surface, configuration)

### Implemented on `claude/compassionate-keller-jnSqo`

1. **README expansion**. The previous README was a thin Quick Start. The rewrite adds:
   - An architecture diagram showing the FE → FastAPI → CrewAI → (Tavily, LiteLLM, ChromaDB) flow.
   - A real project-structure tree.
   - An API surface table.
   - A configuration table covering `ANTHROPIC_API_KEY`, `TAVILY_API_KEY`, `LITELLM_MODEL`, `CHROMA_DB_PATH`, `BACKEND_URL`.
   - A note that the default branch is `master` (not `main`) so contributors don't trip on it.
2. **Top-level `.env.example`**. The repo only had `backend/.env.example` (39 bytes) with two keys and no comments. Added a richer top-level template with examples for LiteLLM model overrides and ChromaDB / backend-URL settings, while keeping the same key names so existing setups still work.
3. **This `RESEARCH_LOG.md`**.

### Why these were prioritized

- The original README claimed the system uses NVIDIA NIM, but `backend/.env.example` actually wires up `ANTHROPIC_API_KEY`. That contradiction is a bad first impression. The new README explains the LiteLLM provider model honestly: Claude by default, anything else via `LITELLM_MODEL`.
- All changes are documentation-only. Zero risk of breaking existing functionality.
- Showcase enhancement matches the brief: this project is technically interesting (multi-agent + RAG + psych frameworks) but underdocumented.

### Evaluated and skipped this run

- **CI workflow.** Considered adding GitHub Actions for `npm run build` + backend smoke tests. Skipped because there are no real backend tests yet — the existing `test_env.py` and `test_gemini.py` are env-checks, not pytest cases.
- **Dockerfile / docker-compose.** Real value, but requires testing both Python and Node builds. Logged as next-run candidate.
- **Frontend audit (lint, type-check).** Out of scope without local execution.
- **Switching the README away from "NVIDIA NIM"-only language.** Done implicitly via the new LiteLLM-provider explanation.

### Next-run candidates

- Add a real pytest suite around the FastAPI route and the CrewAI pipeline (mocked LLM provider).
- Add `Dockerfile` + `docker-compose.yml` (backend + frontend + chroma persistence volume).
- Add a GitHub Actions workflow: backend pip install + pytest, frontend `npm ci && npm run build`.
- Persist run results to SQLite so prospect reports survive restarts.
- Add a streaming SSE endpoint so the FE can render agent traces live.
